import json

goldFile="corpora/json/linking/thomas.json"
predFile =""


with open(goldFile) as f:
    goldDocuments = json.load(f)
f.close()

with open(predFile) as f:
    predDocuments = json.load(f)
f.close()

