import os
import glob
import json

inDir="corpora/original/SETH/"
outFile="corpora/json/SETH.json"

corpusDict = {}
corpusFile = open(inDir + "corpus.txt", 'r')
for line in corpusFile:
    line = line .strip()
    #print(line)

    array = line.split("\t")
    if(len(array) != 2):
        print("Error reading corpusline '" +line +"'")

    corpusDict[array[0]] = array[1]

corpusFile.close()

jsonDocuments = []
for filepath in glob.iglob(inDir +'/annotations/*.ann'):
        #print(filepath)
        annotationFile = open(filepath, 'r')
        pubmedId = os.path.basename('corpora/original/SETH//annotations/8460646.ann').rsplit('.', 1)[0]

        entities = []
        relations = []
        for line in annotationFile:
            line = line.strip()
            if(line == ""):
                continue
            #print(line)

            array = line.split()

            if (array[0].startswith("T")):
                entities.append({"ID": array[0], "type":array[1], "begin" : array[2], "end" : array[3], "text" : " ".join(array[4:])})

            elif (array[0].startswith("R")):
                if(len(array) != 4):
                    print("Error reading annotationfile '"+filepath)
                    print(array)
                else:
                    relations.append({"ID" : array[0], "type" : array[1], "arg1" : array[2], "arg2" : array[3]})
            else:
                print("No handling for '" +line +"' in: " +filepath)

        jsonDocument = {"document" : {
            "ID" : pubmedId,
            "text" : corpusDict[pubmedId],
            "entities" : entities,
            "relations" : relations
        }}
        jsonDocuments.append(jsonDocument)

        annotationFile.close()


f = open(outFile, "w")
f.write(json.dumps(jsonDocuments, indent=4))
f.close()

