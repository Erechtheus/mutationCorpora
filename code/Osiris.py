import json
import xml.etree.ElementTree as ET
inFile = "corpora/original/Osiris/OSIRIScorpusv01.xml"
outFile="corpora/json/linking/osiris.json"

tree = ET.parse(inFile)
root = tree.getroot()

jsonDocuments = []
for article in root.findall("Article"):
    pmid = article.find("Pmid").text

    titleElement = article.find("Title")
    abstractElement = article.find("Abstract")

    text = ""
    if titleElement.text is not None:
        text = titleElement.text

    annotations = []

    #Handle title
    for children in list(titleElement):
        if children.tag == "gene":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(text), "end": len(text) + len(children.text),
             "text": children.text, "entrez": children.get("g_id"), })

        elif children.tag == "variant":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(text),
                                "end": len(text) + len(children.text),
                                "text": children.text, "dbSNP": children.get("v_id"), })

        else:
            print("Error no handling for '" +children.tag +"'")

        text = text +children.text
        if children.tail is not None:
            text = text + children.tail

    #Handle abstract
    text = text +"\n"
    if abstractElement.text is not None:
        text = abstractElement.text


    for children in list(abstractElement):
        if children.tag == "gene":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(text), "end": len(text) + len(children.text),
             "text": children.text, "entrez": children.get("g_id")})

        elif children.tag == "variant":
            annotations.append({"ID": "T" + str(len(annotations)), "type": children.tag, "begin": len(text),
                                "end": len(text) + len(children.text),
                                "text": children.text, "dbSNP": children.get("v_id")})

        else:
            print("Error no handling for '" +children.tag +"'")

        text = text +children.text
        if children.tail is not None:
            text = text + children.tail

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

