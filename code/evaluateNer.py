from nervaluate import Evaluator
import json
import argparse

if __name__ == "__main__":
    print("Evaluation of named entity recogntion")

    # Parse the arguments from the command line
    parser = argparse.ArgumentParser(description='Evaluate Named Entity Recognition performance')
    parser.add_argument('gold', nargs='?', help='Destination of gold-file')
    parser.add_argument('prediction', nargs='?', help='Destination of predicted file')
    args = parser.parse_args()
    #main(args.config)

goldFile="corpora/json/linking/mutationCoreference.json"
predFile ="corpora/json/linking/mutationCoreference.json"


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
        docID = document["document"]["ID"]
        docEntities = document["document"]["entities"]

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
evaluator = Evaluator(trueLabel, predLabel, tags=list(set([item["label"] for sublist in predLabel for item in sublist])))
results, results_per_tag = evaluator.evaluate()
print("Goldstandard = " +goldFile)
print("Predicted-file= " +predFile)
print("------------------")
print(results)