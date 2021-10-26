import os
import glob
import json

inDir = "corpora/original/amia-18-mutation-corpus-master/data/"

for folder in sorted(os.listdir(inDir)):

    if os.path.isdir(os.path.join(inDir,folder)):
        jsonDocuments = []

        #1.) Load all txt files
        corpusDict = {}
        for filepath in glob.iglob(os.path.join(inDir,folder) + '/*.txt'):
            pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

            file = open(filepath, mode='r')
            content = file.read()
            file.close()

            corpusDict[pubmedId] = content

        #2.) Load the annotations
        for filepath in glob.iglob(os.path.join(inDir, folder) + '/*.ann'):
            pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

            entities = []
            relations = []
            annotationFile = open(filepath, 'r')
            for line in annotationFile:
                array = line.strip().split()
                print(array)

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


        """            
        corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
            "documents" : jsonDocuments}
        
        f = open(outFile, "w")
        f.write(json.dumps(corpus, indent=4))
        f.close()
        """