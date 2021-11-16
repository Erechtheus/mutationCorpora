import json
import xml.etree.ElementTree as ET
inFile = "corpora/original/Osiris/OSIRIScorpusv01.xml"
outFile="corpora/json/linking/osiris.json"

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
                                "text": children.text, "dbSNP": children.get("v_id") })
            else:
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(titleText),
                                "end": len(titleText) + len(children.text),
                                "text": children.text })

        else:
            print("Error no handling for '" +children.tag +"'")

        titleText = titleText +children.text
        if children.tail is not None:
            titleText = titleText + children.tail

    # Minor error analysis
    for annotation in annotations:
        if annotation["text"] != titleText[annotation["begin"]:annotation["end"]]:
            print(annotation["text"])

            print(titleText[annotation["begin"]:annotation["end"]])
            print("---")



    # 2.) Handle abstract
    abstractText = ""
    if abstractElement.text is not None:
        abstractText = abstractElement.text

    annotations = []

    for children in list(abstractElement):
        if children.tag == "gene":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(abstractText), "end": len(abstractText) + len(children.text),
             "text": children.text, "entrez": children.get("g_id"), })

        elif children.tag == "variant":
            if children.get("v_id").isnumeric():  # Otherwise entity cannot be normalized to dbSNP
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(abstractText),
                                "end": len(abstractText) + len(children.text),
                                "text": children.text, "dbSNP": children.get("v_id") })
            else:
                annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(abstractText),
                                "end": len(abstractText) + len(children.text),
                                "text": children.text })

        else:
            print("Error no handling for '" +children.tag +"'")

        abstractText = abstractText +children.text
        if children.tail is not None:
            abstractText = abstractText + children.tail

    # Minor error analysis
    for annotation in annotations:
        if annotation["text"] != abstractText[annotation["begin"]:annotation["end"]]:
            print(annotation["text"])

            print(abstractText[annotation["begin"]:annotation["end"]])
            print("---")

    jsonDocument = {"document": {
        "ID": pmid,
        "text": text,
        "entities": annotations,
        "relations": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()

