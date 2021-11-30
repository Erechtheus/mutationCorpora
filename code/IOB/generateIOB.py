import json
import os
from pathlib import Path
import spacy # #python -m spacy download en_core_web_sm

nlp = spacy.load('en_core_web_sm')


randomSeed = 1202
splitSize = 80 / 100
inFolder="corpora/json/"
splitFolder="code/IOB/splits/"
iobFolder="code/IOB/IOB/"

def is_overlapping(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)

if __name__ == "__main__":
    print("Generate IOB files using the train/test splits")

for path in Path(inFolder).glob('*.json'):

    print(path)

    folderName = os.path.basename(path)
    folderName = folderName[:-5]

    #Skip corpora with dedicated train/test splits (e.g., AMIA or tmvar)
    if "train" in folderName or "test" in folderName:
        continue

    with open(splitFolder +folderName +".json") as f:
        splits = json.load(f)
    f.close()


    with open(path) as f:
        corpus = json.load(f)
    f.close()

    iobString = "Word,Tag\n"
    for document in corpus["documents"]:
        docID = document["document"]["ID"]
        docText = document["document"]["text"]
        docEntities = document["document"]["entities"]

        iobString = iobString +"#"  +docID +"\n"

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
                    token =tokens[tokenIndex]
                    tokenStart = token.idx
                    tokenEnd = token.idx + len(token.text)

                    if is_overlapping(entityStart, entityEnd, tokenStart, tokenEnd):
                        markAsEntity.append(tokenIndex)


                    for marker in range(len(markAsEntity)):
                        markIndex=markAsEntity[marker]

                        if marker == 0:
                            labels[markIndex] = "B-" +entityTpe

                        else:
                            labels[markIndex] = "I-" +entityTpe

            for tokenIndex in range(len(tokens)):
                iobString = iobString + str(tokens[tokenIndex]) +"," +labels[tokenIndex] +"\n"
            iobString = iobString +" , \n"#next sentence

    #print(iobString)


def generateIOB(document, entities):
    print("A")