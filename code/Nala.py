import os
import glob
import json


inDir="corpora/original/Nala/tagtog_IDP4/"
outFile="corpora/json/tagtog_IDP4.json"

for filepath in glob.glob(inDir +'/**/*.ann.json', recursive=True):
    with open(filepath, 'r') as myfile:
        data = json.loads(myfile.read())

        pmid = -1
        for source in data["sources"]:
            if source["name"] == "PMID":
                pmid = source["id"]

        if pmid == -1:
            print("No pmid found!")

        if data["anncomplete"] == False:
            print("Skipping document, annotation incomplete")
            continue

        entities = data["entities"]
        relations = data["relations"]
