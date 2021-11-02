import json

goldFile="corpora/json/linking/thomas.json"
predFile =""

snpDict = {}
def getMerge(rsId):
    if rsId not in snpDict:
        response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&rettype=json&retmode=text&id=" +str(rsId))
    if resp.status_code == 200:
        snpDict[response.json()["refsnp_id"]] = set(map(lambda x : x["merged_rsid"], response.json()["dbsnp1_merges"]))
    print(snpDict)
    return snpDict[rsId]

with open(inFile) as f:
    documents = json.load(f)
    for document in documents["documents"]:
        filter entities without rs :-)
f.close()