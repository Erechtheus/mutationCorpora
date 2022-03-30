from jsonschema import validate
import json

f = open('code/jsonschema/schema/corpus.json')
corpusSchema = json.load(f)
f.close()

# We dissalow missing entity text
validate(instance={
    "referenceURL": "http",
    "version": "V1.0",
    "bibtex": "dsds",
    "documents" : []
},
         schema=corpusSchema)
