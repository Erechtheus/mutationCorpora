import os
import json
import xml.etree.ElementTree as ET
from tools.fetchTool import getPMID

inFile="../corpora/original/Thomas2011/annotations.txt"
outFile="../corpora/json/linking/thomas.json"

if __name__ == "__main__":
    print("Converting Thomas2011 corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


#1.) Load annotations
annotationDict = {}
corpusFile = open(inFile, 'r')
for line in corpusFile:
    array = line.strip().split("\t")
    #print(array)

    if(len(array) != 7):
        print("Error!")

    if array[0] not in annotationDict:
        annotationDict[array[0]] = []

    annotationDict[array[0]].append({"ID": "T" + str(len(annotationDict[array[0]])),  "begin": int(array[3]) , "end": int(array[4]) , "text": array[1][1:-1], "dbSNP" : int(array[5].split("rs")[1]), "type" : array[6]})
corpusFile.close()

#2.) Get the documents from NCBI eutils
#We cache the result in cacheFile for faster processing
documentDict = getPMID(annotationDict.keys())

errors = 0
errorDocs = set()
#3.) Build the documents for JSON serializaion
jsonDocuments = []
for pmid in annotationDict.keys():

    root = ET.fromstring(documentDict[pmid])
    title = root.find("PubmedArticle").find("MedlineCitation").find("Article").find("ArticleTitle").text
    #We modify titles which are encapsulated in a [].
    if title.startswith("[") and title.endswith("]."):
        title = title[1:-2]

    abstr = ""
    for abstract in root.find("PubmedArticle").find("MedlineCitation").find("Article").find("Abstract").findall("AbstractText"):
        #Add the label of an abstract section, if it is not the tag unlabelled
        if "Label" in abstract.keys() and abstract.get("Label") != "UNLABELLED":
            abstr +=  abstract.get("Label")
            abstr += "  "

        abstr += (abstract.text)
        abstr += "\n"

    documentText = title +"\n\n" +abstr
    #print(documentText)

    for annotation in annotationDict[pmid]:
        if annotation["text"] != documentText[annotation["begin"] : annotation["end"]]:
            print(pmid)
            print("'" +annotation["text"] +"' != '" +documentText[annotation["begin"] : annotation["end"]] +"'")
            print(annotation)
            print(title +"\n" +abstr)
            print("----")
            errors = errors +1
            errorDocs.add(pmid)

    jsonDocument = {"document": {
        "ID": pmid,
        "text": documentText,
        "entities": annotationDict[pmid],
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

#Print some errors
print("No errors= " +str(errors) +" in " +str(len(errorDocs))  +" documents=" +str(errorDocs))