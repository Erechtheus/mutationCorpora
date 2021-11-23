import json
import os
from pathlib import Path

"""

* start brat container:  
```shell script
docker run --name=brat -d -p 81:80 -v ~/.brat/data:/bratdata -v ~/.brat/config:/bratcfg -e BRAT_USERNAME=brat -e BRAT_PASSWORD=brat -e BRAT_EMAIL=brat@example.com cassj/brat
```
* update brat data with corpus:
```shell script
sudo rm -rf ~/.brat/data/corpus
sudo cp -r YOUR_LOCAL_CORPUS_LOCATION ~/.brat/data/corpus
sudo chmod -R 755 ~/.brat/data/corpus
sudo chown -R www-data:www-data ~/.brat/data/corpus
```

"""

inFolder="../corpora/json/"
outFOlder="../corpora/BRAT/"


if __name__ == "__main__":
    print("Export all corpora into BRAT format")

for path in Path(inFolder).rglob('*.json'):
    folderName = os.path.basename(path)
    folderName = folderName[:-5]

    #Create export-directories if necessary
    if os.path.isdir(outFOlder +folderName) == False:
        os.mkdir(outFOlder +folderName)

    with open(path) as f:
        corpus = json.load(f)
    f.close()

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

        for relation in relations:
            f.write(relation["ID"])
            f.write("\t")
            f.write(relation["type"])
            f.write("\t")
            f.write("Arg1:")
            f.write(relation["arg1"])
            f.write(" ")
            f.write("Arg2:")
            f.write(relation["arg2"])
            f.write("\n")

        f.close()
