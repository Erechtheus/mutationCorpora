import json
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

inFolder="corpora/json/"
outFOlder="corpora/BRAT/"


if __name__ == "__main__":
    print("Executing")

for path in Path(inFolder).rglob('*.json'):
    with open(path) as f:
        corpus = json.load(f)
    f.close()

    for document in corpus["documents"]:
        id = document["document"]["ID"]
        text = document["document"]["text"]
        entities = document["document"]["entities"]
        relations = document["document"]["relations"]