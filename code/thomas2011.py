import json
import requests
import xml.etree.ElementTree as ET
inFile="corpora/original/Thomas2011/annotations.txt"
outFile="corpora/json/linking/thomas.json"


#1.) Load annotations
annotaitonDict = {}
corpusFile = open(inFile, 'r')
for line in corpusFile:
    array = line.strip().split("\t")
    #print(array)

    if(len(array) != 7):
        print("Error!")

    if array[0] not in annotaitonDict:
        annotaitonDict[array[0]] = []

    annotaitonDict[array[0]].append({"ID": "T"+ str(len(annotaitonDict[array[0]])), "type": array[1], "begin": array[3], "end": array[4], "text": array[2], "dbSNP" : array[5], "type" : array[6]})
corpusFile.close()

#2.) Get the documents from NCBI eutils
jsonDocuments = []
for pmid in annotaitonDict.keys():
    print(pmid)

    response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=xml&id="+pmid)

    root = ET.fromstring(response.text)
    title = root.find("PubmedArticle").find("MedlineCitation").find("Article").find("Journal").find("Title").text
    abstr = root.find("PubmedArticle").find("MedlineCitation").find("Article").find("Abstract").find("AbstractText").text

    jsonDocument = {"document": {
        "ID": pmid,
        "text": title +"\n" +abstr,
        "entities": annotaitonDict[pmid],
        "relations": [],
        "metadata": []
    }}
    jsonDocuments.append(jsonDocument)


corpus = {"referenceURL" : "", "version" : "", "bibtex" : "",
    "documents" : jsonDocuments}

f = open(outFile, "w")
f.write(json.dumps(corpus, indent=4))
f.close()

