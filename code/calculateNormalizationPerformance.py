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



performances = {} #We save TP, FP, FN for each mutation-type in this variable
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

            if goldType not in  performances:
                performances[goldType] = {}
                performances[goldType]["tp"] = 0
                performances[goldType]["fp"] = 0
                performances[goldType]["fn"] = 0

            #Search the respective prediction doocument
            predDocument = list(filter(lambda x : x["ID"] == documentID, predDocuments))
            if len(predDocument) != 1:
                print("Should not happen! We found " +str(len(predDocument)) +" != 1 documents for " +str(documentID))

            else:
                #Search the respective prediction for the entity
                predEntity = list(filter(lambda x : x["ID"] == goldID, predDocument[0]["entities"] ))
                if len(predEntity) > 1:
                    print("Should not happen! We received more than one entity with ID='" +str(goldID) +"'")

                # If we find not the entity or if the returned entity has no rs-ID -> FN
                elif len(predEntity) == 0 or len(predEntity[0]["rs"]) ==0:
                    performances[goldType]["fn"] = performances[goldType]["fn"] + 1

                #In this case we have at least one prediction for the named entity
                else:
                    predictedRSs = set(predEntity[0]["rs"])

                    print(documentID +"\t" +goldID +"\trs=" +str(goldRS) +"\t" +str(predictedRSs))


                    if goldRS in predictedRSs:
                        performances[goldType]["tp"] = performances[goldType]["tp"] +1
                        predictedRSs.remove(goldRS)
                        print("TP")
                    else:
                        performances[goldType]["fn"] = performances[goldType]["fn"] +1
                        print("FN")

                    if len(predictedRSs) > 0:
                        performances[goldType]["fp"] = performances[goldType]["fp"] +len(predictedRSs)
                        print("FP")


for key in performances.keys():
    tp = performances[key]["tp"]
    fp = performances[key]["fp"]
    fn = performances[key]["fn"]

    print("------" +key +"------")
    print("TP=" +str(tp))
    print("FP=" +str(fp))
    print("FN=" +str(fn))

    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1  =  2*(recall * precision) / (recall + precision)
    print("Precision=%.2f" % precision )
    print("Recall=%.2f" %recall)
    print("F1=%.2f" %f1)



