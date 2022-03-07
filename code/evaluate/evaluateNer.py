from nervaluate import Evaluator
import json
import argparse
import os

# --gold /home/philippe/workspace/PycharmProjects/mutationCorpora/corpora/json/amia-test.json --prediction /home/philippe/workspace/PycharmProjects/mutationCorpora/corpora/predictions/ner/predictions.json
# --gold /home/philippe/workspace/PycharmProjects/mutationCorpora/corpora/json/amia-test.json --prediction /home/philippe/workspace/PycharmProjects/mutationCorpora/corpora/predictions/ner/predictions_run_25_02_22_12_06.json
#Parse arguments from command line
parser = argparse.ArgumentParser(description='Evaluate Named Entity Recognition performance')
parser.add_argument('--gold', required=True, type=str, nargs='?', help='Destination of gold-file')
parser.add_argument('--prediction', required=True, type=str, nargs='?', help='Destination of predicted file')
args = parser.parse_args()
if args.gold:
    goldFile = args.gold

if args.prediction:
    predFile = args.prediction


if __name__ == "__main__":
    print("Evaluation of named entity recognition (NER)")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


# Code to convert our internal representation for named entities into
# the required format from nervaluate
def convertEntitiesToNervaluate(entities):
    result = []

    for entity in entities:
        result.append({"label": entity["type"], "start": entity["begin"], "end": entity["end"]})
    return result

# Loads a corpus from a file and stores the entities in a key-value map
# The key in this map is the identifier of the document and the values
# are the entities in the document
def loadDocumentsToMap(filename):

    #Load JSON
    with open(filename) as f:
        documents = json.load(f)
    f.close()

    #Parse JSON
    tmpMap = {}
    for document in documents["documents"]:

        #This is the normal structure for gold-annotations
        if "document" in document:
            docID = document["document"]["ID"]
            docEntities = document["document"]["entities"]
        #This is an alternative structure for predictions
        else:
            docID = document["ID"]
            docEntities = document["predicted_entities"]

        if docID in tmpMap:
            print("Multiple entries for '" +docID +"' in '" +filename +"'")
        else:
            tmpMap[docID] = convertEntitiesToNervaluate(docEntities)

    return tmpMap


goldMap = loadDocumentsToMap(goldFile)
predMap = loadDocumentsToMap(predFile)

#CHeck if we have predictions which are not expecting
#if predMap.keys() not in goldMap.keys():
#    print("Hmm")

#Now we generate the final representation for nervaluate
trueLabel = []
predLabel = []
for docId in goldMap.keys():
    trueLabel.append(goldMap[docId])

    if docId in predMap:
        predLabel.append(predMap[docId])
    else: #If we have no predictions, add this
        predLabel.append([])


# Evaluate and print result
tags = list(set([item["label"] for sublist in predLabel for item in sublist]))
evaluator = Evaluator(trueLabel, predLabel, tags=tags)
results, results_per_tag = evaluator.evaluate()
print("Goldstandard = " +goldFile)
print("Predicted-file= " +predFile)
print(tags)
print("------------------")
#print(results)
print(json.dumps(results_per_tag, sort_keys=True, indent=4))