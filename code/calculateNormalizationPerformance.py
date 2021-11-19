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
for goldDocument in goldDocuments["documents"]:
    for goldEntity in goldDocument["document"]["entities"]:
        if "dbSNP" in goldEntity:
            dbSNPIDs.add(str(goldEntity["dbSNP"]))
snpDict = getSNPs(dbSNPIDs)

dbSNPIDs = set()
for goldDocument in predDocuments:
    for goldEntity in goldDocument["entities"]:
        for x in goldEntity["rs"]:
            dbSNPIDs.add(str(x))
snpDict = getSNPs(dbSNPIDs)
####</Retrieve all dbSNP Ids>####



tp = 0
fp = 0
fn = 0
#Iterate the goldstandard
for goldDocument in goldDocuments["documents"]:
    documentID = goldDocument["document"]["ID"]

    #Iterate all entities in the goldDocument
    for goldEntity in goldDocument["document"]["entities"]:
        #Do we have a goldstandard for this NE?
        if "dbSNP" in goldEntity:
            goldID = goldEntity["ID"]           #The ID of the entity (e.g., T0, T1, ...)
            goldRS = goldEntity["dbSNP"]        #The correct dbSNP-ID
            goldType = goldEntity["type"]       #The type of the mutation

            #Search the respective prediction doocument
            predDocument = list(filter(lambda x : x["ID"] == documentID, predDocuments))
            if len(predDocument) != 1:
                print("SHould not happen! We found " +str(len(predDocument)) +" != 1 documents for " +str(documentID))

            else:
                #Search the respective prediction for the entity
                predEntity = list(filter(lambda x : x["ID"] == goldID, predDocument[0]["entities"] ))
                if len(predEntity) > 1:
                    print("SHould not happen! We received more than one entity with ID='" +str(goldID) +"'")
                # If we find not the entity and if the entity has no rs-ID -> FN
                elif len(predEntity) == 0 or len(predEntity[0]["rs"]) ==0:
                    fn = fn +1

                #In this case we have at least one prediction for the named entity
                else:
                    predictedRSs = predEntity[0]["rs"]

                    tmpTP = False
                    tmpFP = False
                    tmpFN = False

                    print(documentID +"\t" +goldID +"\trs=" +str(goldRS) +"\t" +str(predictedRSs))

                    if goldRS in predictedRSs:
                        tp = tp +1
                    if goldRS not in predictedRSs:
                        fn = fn + 1


print("TP=" +str(tp))
print("FP=" +str(fp))
print("FN=" +str(fn))

precision = tp/(tp+fp)
recall = tp/(tp+fn)
f1  =  2*(recall * precision) / (recall + precision)
print("Precision=%.2f" % precision )
print("Recall=%.2f" %recall)
print("F1=%.2f" %f1)



