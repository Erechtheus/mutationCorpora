import requests
import os
import pickle
from tqdm import tqdm
import json
import xml.etree.ElementTree as ET
import wget
import gzip

# Get the documents from NCBI eutils
# We cache the result in cacheFile for faster processing
def getPMID(pmids):
    print("Fething" +str(len(pmids)) +"pubmed abstracts")

    cacheFolder = "../cache/"
    cacheFile = cacheFolder + "thomas.pickle"

    documentDict = {}
    if os.path.isdir(cacheFolder) == False:
        os.mkdir(cacheFolder)

    if os.path.exists(cacheFile):
        with open(cacheFile, 'rb') as file:
            documentDict = pickle.load(file)
    else:
        for pmid in pmids:
            print("Fetching '" + str(pmid) + "' from NCBI utils")
            response = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id=" + pmid)
            documentDict[pmid] = response.text

        with open(cacheFile, 'wb') as fid:
            pickle.dump(documentDict, fid)
        fid.close()

    return documentDict

# The methods getSNPFromRsMergeArch, getSNPFromXML, getSNPs do all the same!
# They all try to find the merge information for a dbSNP-mention. For example,  rs3168321 -> rs334
# However, the REST-Endpoints have their own problems. For instance some return no result when >= 1 ID is non existant
# In the end we decided tp use the RsMergeArch-file provided by dbSNP which publishes the whole history of dbSNP-merges
def getSNPFromRsMergeArch(dbSNPIDs):

    cacheFolder = "../cache/"
    url = "ftp://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/database/organism_data/RsMergeArch.bcp.gz"
    RsMergeArchFile = cacheFolder + "RsMergeArch.bcp.gz"
    cacheFile = cacheFolder + "dbSNP.pickle"

    dbSNPIDs = set(map(int, dbSNPIDs))  # Ensure that the IDs are a set and integers

    if os.path.isdir(cacheFolder) == False:
        os.mkdir(cacheFolder)

    if not os.path.exists(RsMergeArchFile):
        print(RsMergeArchFile +" not found, downloading")
        wget.download(url, RsMergeArchFile)

    if os.path.exists(cacheFile):
        with open(cacheFile, 'rb') as file:
            snpDict = pickle.load(file)
    else:
        snpDict = {}


    #Return loaded snpDict, if there is nothing missing
    dbSNPIDs = dbSNPIDs - set(snpDict.keys())  # We query the webservice only for missing dbSNP-identifiers
    if len(dbSNPIDs) == 0:
        return snpDict

    #Otherwise load file
    print("Parsing RsMergeArchFile")
    with gzip.open(RsMergeArchFile, 'rb') as fin:
        for line in fin:
            line = line.decode('UTF-8')
            line = line.split("\t")
            orig = int(line[0]) #Old-UD
            newId = int(line[1]) #New-ID

            if orig in dbSNPIDs or newId in dbSNPIDs:
                if newId not in snpDict.keys():
                    snpDict[newId] = set()

                snpDict[newId].add(orig)
                snpDict[newId].add(newId)

    #Save the result to disk
    with open(cacheFile, 'wb') as fid:
        pickle.dump(snpDict, fid)

    #For some dbSNP-ID's we have no merge information in the file, because these are corect ones :)
    #E.g., when starting with 334 we will find no merge information, as the ID is correct
    #However, we still want to distinguish these ID's from potentially non-existant ID's
    #To this end we use the REST-API :)
    dbSNPIDs = set(dbSNPIDs) - set(snpDict.keys())#We query the webservice only for missing dbSNP-identifiers
    if len(dbSNPIDs) > 0:
        print("Querying REST-API for remaining set of "+str(len(dbSNPIDs)) +" IDs")
        snpDict = getSNPFromXML(dbSNPIDs)

    return snpDict


#divide list into chunks of size n
def divide_chunks(listIn, n):
    for i in range(0, len(listIn), n):
        yield listIn[i:i + n]

def getSNPFromXML(dbSNPIDs):
    dbSNPIDs = set(map(int, dbSNPIDs))  # Ensure that the IDs are a set and integers
    cacheFolder = "../cache/"
    cacheFile = cacheFolder + "dbSNP.pickle"

    if os.path.isdir(cacheFolder) == False:
        os.mkdir(cacheFolder)

    if os.path.exists(cacheFile):
        with open(cacheFile, 'rb') as file:
            snpDict = pickle.load(file)
    else:
        snpDict = {}

    dbSNPIDs = dbSNPIDs - set(snpDict.keys())#We query the webservice only for missing dbSNP-identifiers

    for dbSNP in tqdm(dbSNPIDs):
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term=rs" +str(dbSNP), timeout=60)
        root = ET.fromstring(response.text)
        tmp = set()
        for dbSNPId in root.find("IdList").findall("Id"):
            tmp.add(int(dbSNPId.text))

        snpDict[int(dbSNP)] = tmp

        with open(cacheFile, 'wb') as fid:
            pickle.dump(snpDict, fid)
    return snpDict


#Retrieves all merge information for a set of dbSNP identifiers
#This opens a REST call to NCBI eutils and therefore takes some time
#Therefore, we save all the result into a cache
# Result is a dictionary with merged ids
def getSNPs(dbSNPIDs):
    dbSNPIDs = set(map(int, dbSNPIDs)) #Ensure that the IDs are a set and integers
    cacheFolder = "../cache/"
    cacheFile = cacheFolder + "dbSNP.pickle"

    if os.path.isdir(cacheFolder) == False:
        os.mkdir(cacheFolder)

    if os.path.exists(cacheFile):
        with open(cacheFile, 'rb') as file:
            snpDict = pickle.load(file)
    else:
        snpDict = {}

    dbSNPIDs = dbSNPIDs - set(snpDict.keys())#We query the webservice only for missing dbSNP-identifiers

    if len(dbSNPIDs) > 0:
        print("Querying NCBI-efetch service for " +str(len(dbSNPIDs)) +" IDs. Please stand-by... " +str(dbSNPIDs))
        print("Calling service "+str(int(len(dbSNPIDs)/10)) +" times")
        for chunk in tqdm(divide_chunks(list(dbSNPIDs), 10)):
            response = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=" + str(
                    ",".join(map(str,chunk))), timeout=60)
            snpDict.update(parseNCBIRequest(response.text)) #Add the elements to the dictionary

            #Save each iteration
            with open(cacheFile, 'wb') as fid:
                pickle.dump(snpDict, fid)

#https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term=rs2066714

    #Perform the same block as before, but this time we call the REST service for each dbSNP seperately
    #In our experiments we observed that the dbSNP webservice has problems when called with 10 ID's and one
    #is not in the database, then it retourned no results at all. --> Therefore, we call the service again
    dbSNPIDs = dbSNPIDs - set(snpDict.keys())#We query the webservice only for missing dbSNP-identifiers
    if len(dbSNPIDs) > 0:
        print("Querying NCBI-efetch service for remaining subset of " +str(len(dbSNPIDs)) +" IDs. Please stand-by...")
        for chunk in list(dbSNPIDs):
            response = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=" + str(chunk),
                timeout=60)

            for jsonString in response.text.split("{\"refsnp_id\""):
                if jsonString != "":
                    snpDict.update(parseNCBIRequest(response.text))
                else: #if we get no returncode
                    snpDict[int(chunk)] = set()

            #Save each iteration
            with open(cacheFile, 'wb') as fid:
                pickle.dump(snpDict, fid)

    return snpDict

#Parses the JSON-line for a NCBI dbSNP request
#e.g., https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=334 or
#e.g., https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=334,123
#The webservice returns no result if one of all submitted ID's is wrong..
def parseNCBIRequest(lines):
    resultDict = {}
    for jsonString in lines.split("{\"refsnp_id\""):
        if jsonString != "":
#            print(jsonString[0:50])
            data = json.loads("{\"refsnp_id\"" + jsonString)
            resultDict[int(data["refsnp_id"])] = set(map(lambda x: int(x["merged_rsid"]), data["dbsnp1_merges"]))
            resultDict[int(data["refsnp_id"])].add(int(data["refsnp_id"]))
    return resultDict

#bla = set()
#bla.add(int(4149313))
#tmp = getSNPs(bla)
#print(tmp)