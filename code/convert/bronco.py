import re
import os
import json


inDir = "corpora/original/BRONCO_20151221/"
outFile= "corpora/json/Bronco.json"
inCorpus = inDir +  "BRONCO_FullText_Tabbed_20150602.txt"
inAnnotations = inDir + "BRONCO_MAPPED_final_20151118.txt"


if __name__ == "__main__":
    print("Converting BRONCO corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


#Parse corpus-file
corpusDict = {}
corpusFile = open(inCorpus, 'r', encoding='unicode_escape') #Hmm, I observe some encoding problems
for line in corpusFile:
    line = line .strip()
    array = line.split("\t")
    if len(array) != 3:
        print("Error")
    corpusDict[array[0]] = array[1] +"\t" +array[2]


#Parse annotation-file
#PMICID	Type	Start	End	Text	Gene	Protein/Gene	TypeOfVar	Mutation	HGVS	Disease	Drug	Cell line
annotationDict = {}
annotationFile = open(inAnnotations, 'r', encoding='unicode_escape') #Hmm, I observe some encoding problems
annotationFile.readline()#Skip header
for line in annotationFile:
    line = line.strip()
    array = line.split("\t")
    if len(array) == 13:
        docId = array[0]
        #type = array[1] #only var
        mutationStart = int(array[2])
        mutationEnd = int(array[3])
        mutationMention = array[4]
        gene = array[5]
        mutationType = array[6] #DNA, Protein, SNP
        mutationSubtype = array[7] #DEL, FS, INS, SNP, SUB
        mutation = array[8]#T|681|I
        hgvs = array[9] #p.Y591H
        disease = array[10]#pancreatic cancer
        drug = array[11]#statins
        cellLine = array[12] #SW620

        # Generate normalized type
        normalizedtype = mutationType
        if normalizedtype == "DNA":
            normalizedtype = "Mutation"
        elif normalizedtype == "Protein":
            normalizedtype = "Mutation"
        elif normalizedtype == "SNP":
            normalizedtype = "dbSNP"
        else:
            print("Problem to normalize: '" + normalizedtype + "'")

        if docId not in annotationDict:
            annotationDict[docId] = []

        annotationDict[docId].append(
            {"ID": "T" + str(len(annotationDict[docId])),
             "begin": int(mutationStart), "end": int(mutationEnd),
             "text": mutationMention, "type": mutationType, "normalizedtype": normalizedtype
             })

    else:
        print("Error, wrong number of elements")


jsonDocuments = []

for docId in corpusDict:

    entities = []

    if docId in annotationDict:
        entities = annotationDict[docId]

    jsonDocument = {"document": {
        "ID": docId,
        "text": corpusDict[docId],
        "entities": entities,
        "relations": [],
        "equivalences": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)

corpus = {"referenceURL": "", "version": "", "bibtex": "",
              "documents": jsonDocuments}


f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()