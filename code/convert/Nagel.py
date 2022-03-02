import os
import glob
import json

inDir="../corpora/original/Nagel/"
outFile="../corpora/json/Nagel.json"

if __name__ == "__main__":
    print("Converting Nagel corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


print("Script works, but entity offset from 'Nagel_GC.standoff.txt' do not match the text in folder 'NagelCorpusText'")
exit()

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
        tmpEntities = annotationDict[pubmedId]

        for i in range(len(tmpEntities)):
            tmpEntities[i]
            entities.append(
                {"ID": "T" + str(i), "type": tmpEntities[i][1], "begin": int(tmpEntities[i][2]), "end": int(tmpEntities[i][3]), "text": tmpEntities[i][7]})



    jsonDocument = {"document": {
        "ID": pubmedId,
        "text": corpusDict[pubmedId],
        "entities": entities,
        "relations": relations,
        "equivalences": [],
        "metadata" : []
    }}
    jsonDocuments.append(jsonDocument)


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()
