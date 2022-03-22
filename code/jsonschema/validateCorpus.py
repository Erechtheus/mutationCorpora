from jsonschema import validate

schema = {
    "title": "Documents",
    "description": "Final corpus representation with entities, relations, and equivalences",
    "type": "object",
    "properties": {
        "referenceURL": {
            "title": "URL",
            "description": "URL-refenences ",
            "type": "string"
        },
        "version": {
            "title": "Version",
            "description": "Version Number (starts with V1.0)",
            "type": "string"
        },
        "bibtex": {
            "title": "Bibtex",
            "description": "Citation in Bibtex format",
            "type": "string"
        },
        "documents": {
            "$ref": "file:code/jsonschema/document.json"
        }
    },
    "required": ["referenceURL", "version", "bibtex"]
}

# We dissalow missing entity text
validate(instance={
    "referenceURL": "http",
    "version": "V1.0",
    "bibtex": "dsds",
    "documents" : []
},
         schema=schema)
