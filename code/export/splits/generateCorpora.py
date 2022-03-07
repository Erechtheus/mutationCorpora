import json
import copy

#1.) SETH
inCorpus = "../../../corpora/json/SETH.json"
inSplit = "../../../corpora/splits/SETH.json"
trainFile = "../../../corpora/json/SETH-train.json"
testFile = "../../../corpora/json/SETH-test.json"

#2.) Variome
inCorpus = "../../../corpora/json/Variome.json"
inSplit = "../../../corpora/splits/Variome.json"
trainFile = "../../../corpora/json/Variome-train.json"
testFile = "../../../corpora/json/Variome-test.json"

#3.) Variome120
inCorpus = "../../../corpora/json/Variome120.json"
inSplit = "../../../corpora/splits/Variome120.json"
trainFile = "../../../corpora/json/Variome120-train.json"
testFile = "../../../corpora/json/Variome120-test.json"

if __name__ == "__main__":
    print("Generate train/test JSON-files")

with open(inCorpus) as f:
    corpus = json.load(f)
f.close()

with open(inSplit) as f:
    splits = json.load(f)
f.close()

trainIDs = splits["trainIDs"]
testIDs = splits["testIDs"]

trainDocuments = copy.deepcopy(corpus)
testDocuments = copy.deepcopy(corpus)

for document in corpus["documents"]:

    id = document["document"]["ID"]
    if id in testIDs:
        trainDocuments["documents"].remove(document)

    if id in trainIDs:
        testDocuments["documents"].remove(document)


if len(trainDocuments["documents"]) + len(testDocuments["documents"]) != len(corpus["documents"]):
    print("Error generating test-corpus")

f = open(trainFile, "w")
f.write(json.dumps(trainDocuments, indent=4))
f.close()

f = open(testFile, "w")
f.write(json.dumps(testDocuments, indent=4))
f.close()

