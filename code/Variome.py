import json
import glob
import os

inDir = "corpora/original/Variome/variome_annotation_corpus/data/"
outFile="corpora/json/Variome.json"

#1.) Load corpus
corpusDict = {}
for filepath in glob.iglob(inDir +'*.txt'):
    pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

    file = open(filepath, mode='r')
    content = file.read()
    file.close()

    corpusDict[pubmedId] = content

#2.) Load annotations
jsonDocuments = []
for filepath in glob.iglob(inDir +'*.ann'):
    pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

    annotationFile = open(filepath, 'r')
    entities = []
    relations = []
    for line in annotationFile:
        array = line.strip().split()
        #print(array)

        if (array[0].startswith("T")):
            entities.append({"ID": array[0], "type": array[1], "begin": int(array[2]), "end": int(array[3]), "text": " ".join(array[4:])})

        elif (array[0].startswith("R")):
            if (len(array) != 4):
                print("Error reading annotationfile '" + filepath)
                print(array)
            else:
                relations.append({"ID": array[0], "type": array[1], "arg1": array[2].split(":")[1], "arg2": array[3].split(":")[1]})
        else:
            print("No handling for '" + line + "' in: " + filepath)

    jsonDocument = {"document": {
        "ID": pubmedId,
        "text": corpusDict[pubmedId],
        "entities": entities,
        "relations": relations,
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)

    annotationFile.close()


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()


