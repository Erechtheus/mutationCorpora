import os
import re
import json
inFile="../corpora/original/tmVarNorm/tmVar.Normalization.txt"
outFile="../corpora/json/linking/tmvarnorm.json"

if __name__ == "__main__":
    print("Converting Amia corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass

corpusFile = open(inFile, 'r')
annotations = []
jsonDocuments = []
for line in corpusFile:
    line = line.strip()
    array = line.split("\t")



    matcher = re.search("^(?P<pmid>[0-9]+)\\|(?P<type>[ta])\\|(?P<text>.+)", line)
    if matcher != None:
        pmid = matcher.group("pmid")
        if matcher.group("type") =="t":
            title =  matcher.group("text")
        elif matcher.group("type") =="a":
            abstr =  matcher.group("text")
        else:
            print("Problem")

    elif len(array) == 7:
        if array[6].startswith("RSID") == False:
            print(array)

        annotations.append({"ID": "T" + str(len(annotations)), "type": array[4], "begin": int(array[1]),
                            "end": int(array[2]),
                            "text": array[3], "dbSNP": int(array[6].split(":")[1]) })

    elif len(array) == 6:
        if array[5].startswith("rs") == False:
            print("Skipping " +line)
        else:
            annotations.append({"ID": "T" + str(len(annotations)), "type": array[4], "begin": int(array[1]),
                            "end": int(array[2]),
                            "text": array[3], "dbSNP": int(array[5].split("rs")[1]) })


    #Reset after parsing an article
    elif line == "":

        jsonDocument = {"document": {
            "ID": pmid,
            "text": title +"\n" +abstr,
            "entities": annotations,
            "relations": [],
            "equivalences": [],
            "metadata": []
        }}
        jsonDocuments.append(jsonDocument)

        pmid  = ""
        title = ""
        abstr = ""
        annotations = []

    else:
        print("Skipping line '" +line +"'")
corpusFile.close()



corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()
