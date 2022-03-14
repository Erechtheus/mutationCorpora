import re
import os
import json


inDir = "../corpora/original/EMU/"
outFile= "../corpora/json/EMU.json"
inCorpus = inDir +  "corpus[EMU]_abstracts.txt"
inAnnotations = inDir + "corpus[EMU]_answers.txt"

if __name__ == "__main__":
    print("Converting EMU corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass

#Parse corpus-file
corpusDict = {}
corpusFile = open(inCorpus, 'r')
for line in corpusFile:
    line = line .strip()
    array = line.split("\t")
    if len(array) != 3:
        print("Error")
    corpusDict[array[0]] = array[1] +"\t" +array[2]

#Parse annotation-file
annotationDict = {}
#PMID	Text Begin	Text End	Text	Gene	DNA/Protein/SNP	Mutation Type	Variation(wt|LOC|mt)	Disease	etc
annotationFile = open(inAnnotations, 'r')
annotationFile.readline()#Skip header
for line in annotationFile:
    line = line.strip()
    array = line.split("\t")
    if len(array) == 8 or len(array) == 9:
        docId = array[0]
        mutationStart = array[1]
        mutationEnd = array[2]
        mutationMention = array[3]
        gene = array[4]
        mutationType = array[5] #DNA|Protein|SNP
        mutationForm = array[6] #DEL|FS|INS|SNP|SUB
        mutationNorm = array[7] #Variation(wt|LOC|mt)
        if len(array) == 9:
            disease = array[8] #LOBULAR CARCINOMA
        else:
            disease = None

        #Generate normalized type
        normalizedtype = mutationType
        if normalizedtype == "DNA":
            normalizedtype = "Mutation"
        elif normalizedtype == "Protein":
            normalizedtype = "Mutation"
        elif normalizedtype =="Protein;DNA":
            normalizedtype = "Mutation"
        elif normalizedtype == "SNP":
            normalizedtype = "dbSNP"
        else:
            print("Problem to normalize: '" + normalizedtype + "'")


        if docId not in annotationDict:
            annotationDict[docId] = []

        if mutationMention == "":
            print("Ignoring annotation without mutation-entity: '" +line +"'")

        #For some mutations, we do not know the offset in the text -> Search for it
        elif (mutationStart.isdigit() and mutationEnd.isdigit()) == False:
            #print("'" +mutationMention +"'")
            mutationMention = mutationMention.strip() #Remove leading and trailing whitespace
            mutationMention = mutationMention.strip("()/,") #Remove leading and trailing clutter
            documentText = corpusDict[docId]


            for start in ([m.start() for m in re.finditer(re.escape(mutationMention), documentText)]):
                mutationStart = start
                mutationEnd = start + len(mutationMention)

                annotationDict[docId].append(
                    {"ID": "T" + str(len(annotationDict[docId])),
                     "begin": int(mutationStart), "end": int(mutationEnd),
                     "text": mutationMention, "type": mutationType, "normalizedtype": normalizedtype
                     })

        else:
            #print("'" +mutationMention +"'")
            annotationDict[docId].append(
                {"ID": "T" + str(len(annotationDict[docId])),
                  "begin": int(mutationStart), "end": int(mutationEnd),
                 "text": mutationMention, "type": mutationType, "normalizedtype": normalizedtype
                 })

    else:
        print("Error" +str((array)))



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