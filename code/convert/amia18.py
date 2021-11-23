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
        equivalences = []
        annotationFile = open(filepath, 'r')
        for line in annotationFile:
            array = line.strip().split()
            #print(array)

            if (array[0].startswith("T")):
                entities.append({"ID": array[0], "type": array[1], "begin": int(array[2]), "end": int(array[3]),
                                 "text": " ".join(array[4:])})

            elif (array[0].startswith("R")):
                if (len(array) != 4):
                    print("Error reading annotationfile '" + filepath)
                    print(array)
                else:
                    relations.append({"ID": array[0], "type": array[1], "arg1": array[2].split(":")[1], "arg2": array[3].split(":")[1]})
            elif (array[0].startswith("*")):
                equivalences.append({"ID": "E" +str(len(equivalences)), "type": "alias", "arg1":line.split()[2], "arg2": line.split()[3]})
#              relations.append(
 #                 {"ID": "alias" +str(len(relations)), "type": "alias", "arg1":line.split()[2], "arg2": line.split()[3]})
            else:
                print("No handling for '" + line + "' in: " + filepath)
        annotationFile.close()

        jsonDocument = {"document": {
            "ID": pubmedId,
            "text": corpusDict[pubmedId],
            "entities": entities,
            "relations": relations,
            "equivalences" : equivalences,
            "metadata": []
        }}
        jsonDocuments.append(jsonDocument)
    return jsonDocuments

trainData= getDocuments(inDir + "00/") + (getDocuments(inDir + "01/")) + (getDocuments(inDir + "02/")) + (getDocuments(inDir + "03/")) +(getDocuments(inDir + "04/"))

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : trainData}

f = open(outDir+"amia-train.json", "w")
f.write(json.dumps(corpus, indent=4))
f.close()



testData = getDocuments(inDir + "05/") + (getDocuments(inDir + "06/")) +(getDocuments(inDir + "07/"))

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : testData}

f = open(outDir+"amia-test.json", "w")
f.write(json.dumps(corpus, indent=4))
f.close()
