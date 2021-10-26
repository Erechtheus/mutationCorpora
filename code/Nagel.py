import os
import glob
import json

inDir="corpora/original/Nagel/"
outFile="corpora/json/Nagel.json"


#1.) Load the corpus into corpusDict
corpusDict = {}
for filepath in glob.iglob(inDir +'NagelCorpusText/*.txt'):
    #print(filepath)
    pubmedId = os.path.basename(filepath).rsplit('.', 1)[0]

    file = open(filepath, mode='r')
    content = file.read()
    file.close()

    corpusDict[pubmedId] = content


#2.) Load the annotations
annotationDict = {}
annotationFile = open(inDir + "Nagel_GC.standoff.txt", 'r')
for line in annotationFile:
    array = line.strip().split("\t")
    #print(array)

    if len(array) != 8:
        print("error")

    if array[0] not in annotationDict:
        annotationDict[array[0]] = []

    annotationDict[array[0]].append(array)
annotationFile.close()

#3.) Generate JSON output
jsonDocuments = []
for pubmedId in corpusDict.keys():
    print(pubmedId)

    entities = []
    relations = []

    if pubmedId in annotationDict:
        for i in range(len(annotationDict[pubmedId])):
            annotation = annotationDict[pubmedId][i]
            print(annotation)
            entities.append({"ID": "T" +str(i), "type":array[1], "begin" : array[2], "end" : array[3], "text" : array[7]})


    jsonDocument = {"document": {
        "ID": pubmedId,
        "text": corpusDict[pubmedId],
        "entities": entities,
        "relations": relations,
        "metadata" : []
    }}
    jsonDocuments.append(jsonDocument)


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()
