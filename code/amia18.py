import os
import glob
import json

inDir = "corpora/original/amia-18-mutation-corpus-master/data/"
outDir="corpora/json/"

def getDocuments(inDir):

    jsonDocuments = []

    # 1.) Load all txt files
    corpusDict = {}
    for filepath in glob.iglob(inDir + '/*.txt'):
        pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

        file = open(filepath, mode='r')
        content = file.read()
        file.close()

        corpusDict[pubmedId] = content

    # 2.) Load the annotations
    for filepath in glob.iglob(inDir + '/*.ann'):
        pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

        entities = []
        relations = []
        annotationFile = open(filepath, 'r')
        for line in annotationFile:
            array = line.strip().split()
            #print(array)

            if (array[0].startswith("T")):
                entities.append({"ID": array[0], "type": array[1], "begin": array[2], "end": array[3],
                                 "text": " ".join(array[4:])})

            elif (array[0].startswith("R")):
                if (len(array) != 4):
                    print("Error reading annotationfile '" + filepath)
                    print(array)
                else:
                    relations.append({"ID": array[0], "type": array[1], "arg1": array[2], "arg2": array[3]})
            else:
                print("No handling for '" + line + "' in: " + filepath)
        annotationFile.close()

        jsonDocument = {"document": {
            "ID": pubmedId,
            "text": corpusDict[pubmedId],
            "entities": entities,
            "relations": relations,
            "metadata": []
        }}
        jsonDocuments.append(jsonDocument)
    return jsonDocuments

trainData= getDocuments(inDir + "00/")
trainData.append(getDocuments(inDir + "01/"))
trainData.append(getDocuments(inDir + "02/"))
trainData.append(getDocuments(inDir + "03/"))
trainData.append(getDocuments(inDir + "04/"))

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : trainData}

f = open(outDir+"amia-train.json", "w")
f.write(json.dumps(corpus, indent=4))
f.close()



testData = getDocuments(inDir + "05/")
testData.append(getDocuments(inDir + "06/"))
testData.append(getDocuments(inDir + "07/"))

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : testData}

f = open(outDir+"amia-test.json", "w")
f.write(json.dumps(corpus, indent=4))
f.close()
