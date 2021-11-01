import json

goldFile="corpora/json/linking/thomas.json"
predFile =""

with open(inFile) as f:
    documents = json.load(f)
    for document in documents["documents"]:
        filter entities without rs :-)
f.close()