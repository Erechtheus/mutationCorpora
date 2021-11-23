import xml.etree.ElementTree as ET
import json

inFile="corpora/original/tmVar/test.BioC.xml"
outFile="corpora/json/tmvar-test.json"

inFile="corpora/original/tmVar/train.BioC.xml"
outFile="corpora/json/tmvar-train.json"


jsonDocuments = []
root = ET.parse(inFile).getroot()
for document in root.findall("document"):
    pubmedId = document.find("id").text

    entities = []
    relations = []
    metadata = []
    text = ""
    for passage in document.findall("passage"):
        for infon in passage.findall("infon"):
            if infon.attrib["key"] == "type":
                passageType = infon.text
            else:
                print("No handling for infon-type: '" +str(infon.attrib) +"'")

        offset = passage.find("offset").text
        passageText = passage.find("text").text
        text = text + passageText +"\n"

        metadata.append({"passageOffset" : offset, "passageText" : passageText})


        for annotation in passage.findall("annotation"):
            entityId = annotation.get("id")
            entityStart = int(annotation.find("location").get("offset"))
            entityEnd = int(annotation.find("location").get("offset")) + int(annotation.find("location").get("length"))
            entityText = annotation.find("text").text
            for infon in annotation.findall("infon"):
                if infon.get("key") == "type":
                    entityType = infon.text
                elif infon.get("key") == entityType:
                    entityMeta = infon.text
                else:
                    print("No handle for mutation-infon")

            entities.append({"ID": "T" +str(entityId), "type":entityType, "begin" : entityStart, "end" : entityEnd, "text" : entityText})


    jsonDocument = {"document": {
        "ID": pubmedId,
        "text": text,
        "entities": entities,
        "relations": relations,
        "equivalences": [],
        "metadata" : metadata
    }}
    jsonDocuments.append(jsonDocument)

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()
