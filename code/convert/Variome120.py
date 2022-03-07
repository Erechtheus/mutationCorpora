import json
import glob
import os

inDir = "../corpora/original/Variome120/"
outFile = "../corpora/json/Variome120.json"

if __name__ == "__main__":
    print("Converting Variome120 corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


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
            normalizedtype = array[1]
            if normalizedtype == "mutation":
                normalizedtype = "Mutation"
            else:
                print("Problem to normalize: '" +normalizedtype +"'")

            entities.append({"ID": array[0], "type": array[1], "normalizedtype" : normalizedtype, "begin": int(array[2]), "end": int(array[3]), "text": " ".join(array[4:])})

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
        "equivalences": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)

    annotationFile.close()


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()


