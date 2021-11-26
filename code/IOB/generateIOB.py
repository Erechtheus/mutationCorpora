import json
import os
from pathlib import Path
import spacy # #python -m spacy download en_core_web_sm

nlp = spacy.load('en_core_web_sm')


randomSeed = 1202
splitSize = 80 / 100
inFolder="../../corpora/json/"
splitFolder="splits/"
iobFolder="IOB"



if __name__ == "__main__":
    print("Generate IOB files using the train/test splits")

for path in Path(inFolder).glob('*.json'):

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

    for document in corpus["documents"]:
        docID = document["document"]["ID"]
        docText = document["document"]["text"]
        docEntities = document["document"]["entities"]

        doc = nlp(docText)

        for sent in doc.sents:  # access sentences
            for token in sent:  # access words/symbols (tokens)
                print((token))
                print(token.idx)