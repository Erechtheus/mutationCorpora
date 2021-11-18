import os
import glob
import json


inDir="corpora/original/Nala/tagtog_IDP4/"
outFile="corpora/json/tagtog_IDP4.json"

#1.) Load the html-documents!
#TODO Implement this
print("LOADING of nala documents not implemented! ")
print("@see github issue 1 (https://github.com/Erechtheus/mutationCorpora/issues/1)")
exit()


corpusDict = {}
for filepath in glob.glob(inDir +'/**/*.plain.html', recursive=True):
    file = open(filepath, mode='r')
    content = file.read()
    file.close()

    #TODO: Here we need to implement a document parser for the html files
    #corpusDict

#2.) Handling of entities and relations
jsonDocuments = []
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

        convertedEntities = []
        convertedRelations = []
        for entity in entities:
            classId = entity["classId"]
            text = entity["offsets"][0]["text"]
            begin = entity["offsets"][0]["start"]
            end = entity["offsets"][0]["start"] + len(text)

            ##e_1 = protein, e_2 = mutation, e_3 = organism
            if classId == "e_1":
                classId = "protein"
            elif classId == "e_2":
                classId = "mutation"
            elif classId == "e_3":
                classId = "organism"
            else:
                print("no handling for '" +classId +"'")

            convertedEntities.append({"ID": "T" +str(len(convertedEntities)), "type": classId, "begin": int(begin), "end": int(end),
                             "text": text})

        for relation in relations:
            classId = relation["classId"]
            involvedEnitities =relation["entities"]
            print(involvedEnitities)

            #r_5 =protein <-> mutation; r_6 = protein <-> organism
            if classId == "r_5":
                classId = "protein<->mutation"
            elif classId == "r_6":
                classId = "protein <-> organism"
            else:
                print("no handling for '" + classId + "'")

            for involvedEnitity in involvedEnitities:
                start, stop=involvedEnitities[0].split("|")[1].split(",")
                start = int(start)
                stop = int(stop)
                result = list(filter(lambda x: x["begin"] == start and x["end"] == stop, convertedEntities))
                if len(result) != 1:
                    print("Should not happen!")
                else:
                    convertedRelations.append({"ID": "R" +str(len(convertedRelations)), "type": classId,
                                               "arg1": result[0]["ID"], "arg2": result[0]["ID"]})



        jsonDocument = {"document" : {
            "ID" : pmid,
            "text" : corpusDict[pmid],
            "entities" : entities,
            "relations" : relations,
            "metadata": []
        }}
        jsonDocuments.append(jsonDocument)

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()