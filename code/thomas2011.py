import json
import requests
import xml.etree.ElementTree as ET
inFile="corpora/original/Thomas2011/annotations.txt"
outFile="corpora/json/linking/thomas.json"


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

    annotationDict[array[0]].append({"ID": "T" + str(len(annotationDict[array[0]])),  "begin": int(array[3]) , "end": int(array[4]) , "text": array[1][1:-1], "dbSNP" : array[5], "type" : array[6]})
corpusFile.close()

#2.) Get the documents from NCBI eutils
documentDict = {}
for pmid in annotationDict.keys():

    print(pmid)
    response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id="+pmid)
    documentDict[pmid] = response.text


#3.) Build the documents for JSON serializaion
jsonDocuments = []
for pmid in annotationDict.keys():

    root = ET.fromstring(documentDict[pmid])
    title = root.find("PubmedArticle").find("MedlineCitation").find("Article").find("ArticleTitle").text

    abstr = ""
    for abstract in root.find("PubmedArticle").find("MedlineCitation").find("Article").find("Abstract").findall("AbstractText"):
        abstr += (abstract.text)
        abstr += "\n"

    documentText = title +"\n\n" +abstr

    for annotation in annotationDict[pmid]:
        if annotation["text"] != documentText[annotation["begin"] : annotation["end"]]:
            print(pmid)
            print("'" +annotation["text"] +"' != '" +documentText[annotation["begin"] : annotation["end"]] +"'")
            print(annotation)
            print(title +"\n" +abstr)
            print("----")

    jsonDocument = {"document": {
        "ID": pmid,
        "text": documentText,
        "entities": annotationDict[pmid],
        "relations": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)

corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()

response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id="+"18201684")
xml = response.text
root = ET.fromstring(xml)