import json
import itertools
from fetchTool import getSNPs

goldFile="../corpora/json/linking/osiris.json"
predFile ="../corpora/predictions/linking/osiris.json"

goldFile="../corpora/json/linking/thomas.json"
predFile ="../corpora/predictions/linking/thomas.json"

goldFile="../corpora/json/linking/tmvarnorm.json"
predFile ="../corpora/predictions/linking/tmvarnom.json"

#goldFile="../corpora/json/linking/"
#predFile ="../corpora/predictions/linking/"

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
            dbSNPIDs.add((goldEntity["dbSNP"]))
snpDict = getSNPs(dbSNPIDs)

dbSNPIDs = set()
for goldDocument in predDocuments:
    for goldEntity in goldDocument["entities"]:
        for x in goldEntity["rs"]:
            dbSNPIDs.add((x))
snpDict = getSNPs(dbSNPIDs)
####</Retrieve all dbSNP Ids>####


#Evaluates if two dbSNP-identifiers are identical.
#However we cannot simply test this using the equivilance relationship, as dbSNP identifiers may change over time
#E.g., rs3168321 became rs334 in revision 106 (3rd July 2002)
#Therefore, we have to allow rs3168321 for rs334
def equals(goldSNP, predSNP):
    seta = set(snpDict[goldSNP])
    setb = set(snpDict[predSNP])

    # If the two sets are disjoint, then the elements cannot be identical
    return not set(seta).isdisjoint(setb)




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
            goldText = goldEntity["text"]

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
                    print("FN\t" + documentID + "\t" + goldID +"\t" +goldText + "\trs=" + str(goldRS) + "\t" + str(set()) + "\t" + goldType)

                #In this case we have at least one prediction for the named entity
                else:
                    predictedRSs = set(predEntity[0]["rs"])

#                    print(documentID +"\t" +goldID +"\trs=" +str(goldRS) +"\t" +str(predictedRSs))


                    tp = False
                    toRemove = set()
                    for predictedRS in predictedRSs:
                        if equals(goldRS, predictedRS):
                            tp = True
                            toRemove.add(predictedRS)
                            print("TP\t" + documentID + "\t" + goldID +"\t" +goldText + "\trs=" + str(goldRS) + "\t" + str(predictedRSs) + "\t"+goldType)

                    predictedRSs = predictedRSs - toRemove

                    if tp == True:
                        performances[goldType]["tp"] = performances[goldType]["tp"] +1
                    else:
                        performances[goldType]["fn"] = performances[goldType]["fn"] +1
                        print("FN\t" +documentID +"\t" +goldID +"\t" +goldText +"\trs=" +str(goldRS) +"\t" +str(predictedRSs)+ "\t"+goldType)

                    if len(predictedRSs) > 0:
                        performances[goldType]["fp"] = performances[goldType]["fp"] +len(predictedRSs)
                        print("FP\t" +documentID +"\t" +goldID +"\t" +goldText +"\trs=" +str(goldRS) +"\t" +str(predictedRSs)+ "\t"+goldType)

def divideWOException(num, denum):
    try:
        return num/denum
    except ZeroDivisionError:
        return 0.0

tpSum = 0
fpSum = 0
fnSum = 0
for key in performances.keys():
    tp = performances[key]["tp"]
    fp = performances[key]["fp"]
    fn = performances[key]["fn"]

    tpSum+= tp
    fpSum+= fp
    fnSum+= fn

    print("------" +key +"------")
    print("TP=" +str(tp))
    print("FP=" +str(fp))
    print("FN=" +str(fn))

    precision = divideWOException(tp,(tp+fp))
    recall = divideWOException(tp,(tp + fn))
    f1 = divideWOException(2 * (recall * precision) , (recall + precision))

    print("Precision=%.2f" % precision )
    print("Recall=%.2f" %recall)
    print("F1=%.2f" %f1)



print("------" +"Overall" +"------")
print("TP=" +str(tpSum))
print("FP=" +str(fpSum))
print("FN=" +str(fnSum))

precision = tpSum / (tpSum + fpSum)
recall = tpSum / (tpSum + fnSum)
f1 = 2 * (recall * precision) / (recall + precision)
print("Precision=%.2f" % precision)
print("Recall=%.2f" % recall)
print("F1=%.2f" % f1)
