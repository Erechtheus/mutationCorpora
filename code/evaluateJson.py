import json
import requests
from tqdm import tqdm
import os
import pickle

inFile="corpora/json/amia-test.json"
inFile="corpora/json/amia-train.json"
inFile="corpora/json/SETH.json"
inFile="corpora/json/tmvar-test.json"
inFile="corpora/json/tmvar-train.json"
inFile="corpora/json/Variome.json"

inFile="corpora/json/linking/osiris.json"
inFile="corpora/json/linking/thomas.json"
inFile="corpora/json/linking/tmvarnorm.json"

#divide list into chunks of size n
def divide_chunks(listIn, n):
    for i in range(0, len(listIn), n):
        yield listIn[i:i + n]


#Retrieves all merge information for a set of dbSNP identifiers
#This opens a REST call to NCBI eutils and therefore takes some time
#Therefore, we save all the result into a cache
# Result is a dictionary with merged ids
def getSNPs(dbSNPIDs):
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
        print("Querying NCBI-efetch service. Please stand-by...")
        for chunk in tqdm(divide_chunks(list(dbSNPIDs), 10)):
            response = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=" + str(
                    ",".join(chunk)), timeout=60)

            for jsonString in response.text.split("{\"refsnp_id\""):
                if jsonString != "":
                    #print(jsonString[0:50])
                    data = json.loads("{\"refsnp_id\"" + jsonString)
                    snpDict[data["refsnp_id"]] = set(
                        map(lambda x: x["merged_rsid"], data["dbsnp1_merges"]))

            #Save each iteration
            with open(cacheFile, 'wb') as fid:
                pickle.dump(snpDict, fid)

    return snpDict


#Read and check corpus
offseterrors = 0
offsetDocuments = set()
with open(inFile) as f:
    documents = json.load(f)

    dbSNPIDs = set()
    for document in documents["documents"]:
        for entity in document["document"]["entities"]:
            if "dbSNP" in entity:
                dbSNPIDs.add(str(entity["dbSNP"]))
    snpDict = getSNPs(dbSNPIDs)


    for document in tqdm(documents["documents"]):

        document = document["document"]

        id = document["ID"]
        text = document["text"]
        entities = document["entities"]
        relations = document["relations"]

        #if document.keys() not in ['ID', 'text', 'entities', 'relations', 'metadata']:
        #    print("unknown key" +str(document.keys()))


        for entity in entities:
            if text[entity["begin"] : entity["end"]] != entity["text"]:
                print("Problem with document '" +str(id) +"' entity offset wrong for '" +entity["text"] +"' != '" +text[entity["begin"] : entity["end"]] +"'")
                print(entity)
                print("---")
                offseterrors = offseterrors+1
                offsetDocuments.add(id)

        #    if "dbSNP" in entity:
        #        if entity["dbSNP"] not in snpDict.keys():
        #            print(" PMID=" +str(id) +" dbSNP-ID= '" +str(entity["dbSNP"]) +"'" +" does not exist for entity=" +str(entity))

        for relation in relations:

            relId = relation["ID"]
            relType = relation["type"]
            relArg1 = relation["arg1"]
            relArg2 = relation["arg2"]

            arg1 = list(filter(lambda x: x["ID"] == relArg1, entities))
            arg2 = list(filter(lambda x: x["ID"] == relArg2, entities))

            if (len(arg1) != 1):
                print("Problem with document '" +str(id) +"' number of relations wrong for relation= " +str(relation))
f.close()

print("#Offseterrors=" +str(offseterrors) +" in " +str(len(offsetDocuments)) +" docs" +str(offsetDocuments))

##Print some small statistics
import itertools
from collections import Counter


print("#docs=" +str(len(documents["documents"])))
entities = list(map(lambda x :x["document"]["entities"], documents["documents"]))
relations = list(map(lambda x :x["document"]["relations"], documents["documents"]))

print("#entities=" +str(len(list(itertools.chain(*entities)))))
print("\ttypes=" + str(Counter(list(map(lambda x:x["type"], list(itertools.chain(*entities)))))))
tmp = Counter(list(map(lambda x:x["text"], list(itertools.chain(*entities)))))
print("\tmostCommonTokens=" +str(tmp.most_common(10)))
tmp = Counter(list(map(lambda x:x["dbSNP"], list(itertools.chain(*entities)))))
print("\tmostCommonRSIDs=" +str(tmp.most_common(10)))

print("#relations=" +str(len(list(itertools.chain(*relations)))))
print("\ttypes=" + str(Counter(list(map(lambda x:x["type"], list(itertools.chain(*relations)))))))
