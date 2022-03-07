import json
import os
from pathlib import Path
import spacy # #python -m spacy download en_core_web_sm

randomSeed = 1202
splitSize = 80 / 100
inFolder="../../corpora/json/"
splitFolder="../../corpora/IOB/splits/"
iobFolder="../../corpora/IOB/IOB/"

if __name__ == "__main__":
    print("Generate IOB files using the train/test splits")

def is_overlapping(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)

def writeStringToFile(fileName, string):
    with open(fileName, "w") as text_file:
        text_file.write(string)

#Generate an IOB representation for a single JSON-document
#Be warned this is extremely hacky code with cubic complexity
#Someone, please implement this better
def generateIOB(document):
    iobString = ""

    docID = document["document"]["ID"]
    docText = document["document"]["text"]
    docEntities = document["document"]["entities"]

    iobString = iobString + "#" + docID + "\n"

    doc = nlp(docText)
    for sent in doc.sents:  # access sentences
        tokens = []
        for token in sent:  # access words/symbols (tokens)
            tokens.append(token)
        labels = ["O"] * len(tokens)

        for entity in docEntities:
            entityStart = entity["begin"]
            entityEnd = entity["end"]
            entityTpe = entity["type"]

            markAsEntity = []
            for tokenIndex in range(len(tokens)):
                token = tokens[tokenIndex]
                tokenStart = token.idx
                tokenEnd = token.idx + len(token.text)

                if is_overlapping(entityStart, entityEnd, tokenStart, tokenEnd):
                    markAsEntity.append(tokenIndex)

                for marker in range(len(markAsEntity)):
                    markIndex = markAsEntity[marker]

                    if marker == 0:
                        labels[markIndex] = "B-" + entityTpe

                    else:
                        labels[markIndex] = "I-" + entityTpe

        for tokenIndex in range(len(tokens)):
            iobString = iobString + str(tokens[tokenIndex]) + "," + labels[tokenIndex] + "\n"
        iobString = iobString + " , \n"  # next sentence

    return iobString



nlp = spacy.load('en_core_web_sm')
for path in Path(inFolder).glob('*.json'):

    folderName = os.path.basename(path)
    folderName = folderName[:-5]
    print(folderName)

    with open(path) as f:
        corpus = json.load(f)
    f.close()


    #Skip corpora with dedicated train/test splits (e.g., AMIA or tmvar)
    if "train" in folderName or "test" in folderName:

        iobString = "Word,Tag\n"
        for document in corpus["documents"]:
            iobString = iobString +generateIOB(document)
        writeStringToFile(iobFolder +folderName +".iob", iobString)

    else:

        with open(splitFolder +folderName +".json") as f:
            splits = json.load(f)
        f.close()

        #Train-split
        trainIOBString = "Word,Tag\n"
        ids = set(splits["trainIDs"])
        for document in list(filter(lambda document: document["document"]["ID"] in ids , corpus["documents"])):
            trainIOBString = trainIOBString + generateIOB(document)

        writeStringToFile(iobFolder +folderName +"-train.iob", trainIOBString)

        #Test-split
        testIOBString = "Word,Tag\n"
        ids = set(splits["testIDs"])
        for document in list(filter(lambda document: document["document"]["ID"] in ids, corpus["documents"])):
            testIOBString = testIOBString + generateIOB(document)

        writeStringToFile(iobFolder +folderName +"-test.iob", testIOBString)