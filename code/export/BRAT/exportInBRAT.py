import json
import os
from pathlib import Path

inFolder="../../../corpora/json/"
outFOlder="../../../corpora/BRAT/"


if __name__ == "__main__":
    print("Export all corpora into BRAT format")

for path in Path(inFolder).rglob('*.json'):
    folderName = os.path.basename(path)
    folderName = folderName[:-5]


    #Create export-directories if necessary
    if os.path.isdir(outFOlder +folderName) == False:
        os.makedirs(outFOlder +folderName)

    with open(path) as f:
        corpus = json.load(f)
    f.close()

    # config file
    annotationFile = open(outFOlder + folderName + "/" + "annotation.conf", "w")
    #1.) entities
    annotationFile.write("[entities]\n")
    bla = list(map(lambda x: x["document"]["entities"], corpus["documents"]))
    for a in set([item["type"] for sublist in bla for item in sublist]):
        annotationFile.write(a)
        annotationFile.write("\n")

    #2.) relations
    annotationFile.write("\n[relations]\n")
    relationArgs = set()
    for document in corpus["documents"]:
        entities = document["document"]["entities"]
        relations = document["document"]["relations"]
        for relation in relations:
            arg1 = list(filter(lambda x: x["ID"] == relation["arg1"], entities))
            arg2 = list(filter(lambda x: x["ID"] == relation["arg2"], entities))

            representaiton = (relation["type"]) + "\tArg1:" + (arg1[0]["type"]) + ", Arg2:" + (arg2[0]["type"])
            relationArgs.add(representaiton)

    for tmp in relationArgs:
        annotationFile.write(str(tmp))
        annotationFile.write("\n")

    annotationFile.write("[events]\n")
    annotationFile.write("[attributes]\n")
    annotationFile.close()


    for document in corpus["documents"]:
        id = document["document"]["ID"]
        text = document["document"]["text"]
        entities = document["document"]["entities"]
        relations = document["document"]["relations"]

        #1.) Text file
        f = open(outFOlder +folderName  +"/" +id +".txt", "w")
        f.write(text)
        f.close()

        #2.) Annotation file
        f = open(outFOlder + folderName + "/" + id + ".ann", "w")

        myCounter = 1
        for entity in entities:
            f.write(entity["ID"])
            f.write("\t")
            f.write(entity["type"])
            f.write(" ")
            f.write(str(entity["begin"]))
            f.write(" ")
            f.write(str(entity["end"]))
            f.write("\t")
            f.write(entity["text"])
            f.write("\n")

            #Write normalization
            if "dbSNP" in entity:
                f.write("N")
                f.write(str(myCounter))
                myCounter += 1
                f.write("\t")
                f.write("Reference ")
                f.write(entity["ID"])
                f.write(" ")
                f.write("dbSNP:")
                f.write(str(entity["dbSNP"]))
                f.write("\t")
                f.write(entity["text"])
                f.write("\n")

        for relation in relations:
            f.write(relation["ID"])
            f.write("\t")
            f.write(relation["type"])
            f.write(" ")
            f.write("Arg1:")
            f.write(relation["arg1"])
            f.write(" ")
            f.write("Arg2:")
            f.write(relation["arg2"])
            f.write("\n")


        if "equivalences" in document["document"].keys():
            equivalences = document["document"]["equivalences"]

            for equivalence in equivalences:
                f.write("*")
                f.write("\t")
                f.write(equivalence["arg1"])
                f.write(" ")
                f.write(equivalence["arg2"])
                f.write("\n")


        f.close()
