import json
import itertools
from fetchTool import getSNPs

goldFile="../corpora/json/linking/thomas.json"
predFile ="../corpora/predictions/linking/thomas.json"

if __name__ == "__main__":
    print("Executing")


with open(goldFile) as f:
    goldDocuments = json.load(f)
f.close()

with open(predFile) as f:
    predDocuments = json.load(f)
f.close()

####<Retrieve all dbSNP Ids>####
dbSNPIDs = set()
for document in goldDocuments["documents"]:
    for entity in document["document"]["entities"]:
        if "dbSNP" in entity:
            dbSNPIDs.add(str(entity["dbSNP"]))
snpDict = getSNPs(dbSNPIDs)

dbSNPIDs = set()
for document in predDocuments:
    for entity in document["entities"]:
        for x in entity["rs"]:
            dbSNPIDs.add(str(x))
snpDict = getSNPs(dbSNPIDs)
####</Retrieve all dbSNP Ids>####



tp = 0
fp = 0
fn = 0
for document in goldDocuments["documents"]:
    documentID = document["document"]["ID"]
    entities = document["document"]["entities"]

    for entity in entities:
        #Do we have a goldstandard for this NE?
        if "dbSNP" in entity:
            goldID = entity["dbSNP"]
            goldType = entity["type"]
            goldID = entity["ID"]


            predDocument = list(filter(lambda x : x["ID"] == documentID, predDocuments))
            if len(predDocument) != 1:
                print("SHould not happen! We found " +str(len(predDocument)) +" != 1 documents for " +str(documentID))

            else:
                predEntity = list(filter(lambda x : x["ID"] == goldID, predDocument[0]["entities"] ))
                if len(predEntity) == 0:
                    fn = fn +1
                elif len(predEntity) > 1:
                    print("SHould not happen! We received more than one entity with ID='" +str(goldID) +"'")
                else:
                    print(predEntity[0]["rs"])



