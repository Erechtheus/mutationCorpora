import requests
import os
import pickle
from tqdm import tqdm
import json

#divide list into chunks of size n
def divide_chunks(listIn, n):
    for i in range(0, len(listIn), n):
        yield listIn[i:i + n]


#Retrieves all merge information for a set of dbSNP identifiers
#This opens a REST call to NCBI eutils and therefore takes some time
#Therefore, we save all the result into a cache
# Result is a dictionary with merged ids
def getSNPs(dbSNPIDs):
    dbSNPIDs = set(map(int, dbSNPIDs)) #Ensure that the IDs are a set and integers
    cacheFolder = "cache/"
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