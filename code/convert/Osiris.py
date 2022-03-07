import os
import json
import xml.etree.ElementTree as ET
inFile = "../corpora/original/Osiris/OSIRIScorpusv01.xml"
outFile="../corpora/json/linking/osiris.json"

if __name__ == "__main__":
    print("Converting Osiris corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


tree = ET.parse(inFile)
root = tree.getroot()

jsonDocuments = []
for article in root.findall("Article"):
    pmid = article.find("Pmid").text

#    if pmid != "15164150":
#        continue

    titleElement = article.find("Title")
    abstractElement = article.find("Abstract")

    # 1.) Handle title
    titleText = ""
    if titleElement.text is not None:
        titleText = titleElement.text

    annotations = []

    for children in list(titleElement):
        if children.tag == "gene":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(titleText), "end": len(titleText) + len(children.text),
             "text": children.text, "entrez": children.get("g_id"), })

        elif children.tag == "variant":
            if children.get("v_id").isnumeric():  # Otherwise entity cannot be normalized to dbSNP
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(titleText),
                                "end": len(titleText) + len(children.text),
                                "text": children.text, "dbSNP": int(children.get("v_id")) })
            else:
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(titleText),
                                "end": len(titleText) + len(children.text),
                                "text": children.text })

        else:
            print("Error no handling for '" +children.tag +"'")

        titleText = titleText +children.text
        if children.tail is not None:
            titleText = titleText + children.tail


    # 2.) Handle abstract
    fulltext = titleText +"\n"
    offset = len(fulltext)
    if abstractElement.text is not None:
        fulltext = fulltext + abstractElement.text

    annotations = []

    for children in list(abstractElement):
        if children.tag == "gene":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(fulltext), "end": len(fulltext) + len(children.text),
             "text": children.text, "entrez": children.get("g_id"), })

        elif children.tag == "variant":
            if children.get("v_id").isnumeric():  # Otherwise entity cannot be normalized to dbSNP
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(fulltext),
                                "end": len(fulltext) + len(children.text),
                                "text": children.text, "dbSNP": int(children.get("v_id")) })
            else:
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(fulltext),
                                "end": len(fulltext) + len(children.text),
                                "text": children.text })

        else:
            print("Error no handling for '" +children.tag +"'")

        fulltext = fulltext +children.text
        if children.tail is not None:
            fulltext = fulltext + children.tail

    jsonDocument = {"document": {
        "ID": pmid,
        "text": fulltext,
        "entities": annotations,
        "relations": [],
        "equivalences": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()

print("Done")