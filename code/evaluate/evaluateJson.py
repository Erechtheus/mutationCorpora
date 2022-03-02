import json
import os
from tools.fetchTool import getSNPFromRsMergeArch

inFile="../corpora/json/amia-train.json"
#inFile="../corpora/json/amia-test.json"
#inFile="../corpora/json/SETH.json"
#inFile="../corpora/json/tmvar-train.json"
#inFile="../corpora/json/tmvar-test.json"
#inFile="../corpora/json/Variome.json"
#inFile="../corpora/json/Variome120.json"

#inFile="../corpora/json/linking/osiris.json"
#inFile="../corpora/json/linking/thomas.json"
#inFile="../corpora/json/linking/tmvarnorm.json"
#inFile="../corpora/json/linking/mutationCoreference.json"

if __name__ == "__main__":
    print("Executing")

"""for inFile in glob.iglob("../corpora/json/linking/" + '/*.json', recursive=True):
    print(inFile)
"""

#Read and check corpus
offseterrors = 0
offsetDocuments = set()
missingDBSNPEntries = set() #We save all mutations, for which we cannot find a dbSNP entiry
with open(inFile) as f:
    documents = json.load(f)

    dbSNPIDs = set()
    for document in documents["documents"]:
        for entity in document["document"]["entities"]:
            if "dbSNP" in entity:
                dbSNPIDs.add(int(entity["dbSNP"]))
    snpDict = getSNPFromRsMergeArch(dbSNPIDs)


    for document in documents["documents"]:

        document = document["document"]

        id = document["ID"]
        text = document["text"]
        entities = document["entities"]
        relations = document["relations"]

        for entity in entities:

            if entity["ID"].startswith("T") == False:
                print("Entity ID '" +entity["ID"] +"' should start with T")

            if text[entity["begin"] : entity["end"]] != entity["text"]:
                print("Problem with document '" +str(id) +"' entity offset wrong for '" +entity["text"] +"' != '" +text[entity["begin"] : entity["end"]] +"'")
                print(entity)
                print("---")
                offseterrors = offseterrors+1
                offsetDocuments.add(id)

            if "dbSNP" in entity:
                if int(entity["dbSNP"]) not in snpDict.keys() or int(entity["dbSNP"]) not in snpDict[entity["dbSNP"]]:
                    missingDBSNPEntries.add(entity["dbSNP"])
                    #print(" PMID=" +str(id) +" dbSNP-ID= '" +str(entity["dbSNP"]) +"'" +" does not exist for entity=" +str(entity))


        for relation in relations:

            if relation["ID"].startswith("R") == False:
                print("Relation ID '" +relation["ID"] +"' should start with R in "+str(id))

            relId = relation["ID"]
            relType = relation["type"]
            relArg1 = relation["arg1"]
            relArg2 = relation["arg2"]

            arg1 = list(filter(lambda x: x["ID"] == relArg1, entities))
            arg2 = list(filter(lambda x: x["ID"] == relArg2, entities))

            if (len(arg1) != 1):
                print("Problem with document '" +str(id) +"' number of relations wrong for relation= " +str(relation))
f.close()

##Print some small statistics
import itertools
from collections import Counter

corpusName = os.path.basename(inFile)[:-5]

entities = list(map(lambda x :x["document"]["entities"], documents["documents"]))
relations = list(map(lambda x :x["document"]["relations"], documents["documents"]))

print("#### Overview of corpus '" +corpusName +"'")
print("```")

#Document
print(str(len(documents["documents"])) +" documents")
print("\tOffseterrors=" +str(offseterrors))
tmp = Counter(list(map(lambda x:x["text"], list(itertools.chain(*entities)))))
print("\tmostCommonTokens=" +str(tmp.most_common(10)))

#Entity
print(str(len(list(itertools.chain(*entities)))) +" entities")
print("\tEntity-types=" + str(Counter(list(map(lambda x:x["type"], list(itertools.chain(*entities)))))))
print("\tUnique dbSNP Mentions:" +str(len(list(map(lambda x:x["dbSNP"], filter(lambda x: "dbSNP" in x, list(itertools.chain(*entities))))))))
tmp = Counter(list(map(lambda x:x["dbSNP"], filter(lambda x: "dbSNP" in x, list(itertools.chain(*entities))))))
print("\tmostCommonRSIDs=" +str(tmp.most_common(10)))
print("\tuniqueRSIDs=" +str(len(set(map(lambda x:x["dbSNP"], filter(lambda x: "dbSNP" in x, list(itertools.chain(*entities))))))))
print("\tFor "+str(len(missingDBSNPEntries))+" dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: " +str(missingDBSNPEntries))

#Relation
print(str(len(list(itertools.chain(*relations)))) +" relations")
print("\ttypes=" + str(Counter(list(map(lambda x:x["type"], list(itertools.chain(*relations)))))))

print("```")