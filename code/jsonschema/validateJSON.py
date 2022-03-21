from jsonschema import validate

entitySchema = {
    "entities" : {
        "description" : "List of named entities",
        "type": "array",
        "minItems": 0,
        "prefixItems" : {
            "ID" : {"type" : "string"},
            "type" : {"type" : "string"},
            "begin" : {"type" : "number"},
            "end" : {"type" :"number"},
            "text" : {"type" : "string"}
        }
    }
}

relationSchema = {
    "relations" : {
        "description" : "List of relations",
        "type": "array",
        "minItems": 0,
        "prefixItems" : {
            "ID" : {"type" : "string"},
            "type" : {"type" : "string"},
            "arg1" : {"type" : "number"},
            "arg2" : {"type" :"number"}
        }
    }
}

equivalenceSchema = {
    "equivalences": {
        "description": "List of equivalences",
        "type": "array",
        "minItems": 0,
        "prefixItems": {
            "ID": {"type": "string"},
            "type": {"type": "string"},
            "arg1": {"type": "number"},
            "arg2": {"type": "number"}
        }
    }
}

documentSchema = {
  "title": "Document",
  "description": "A simple document",
  "type": "object",
  "properties": {
      "ID" : {"type": "string"},
      "text" : {"type": "string"},
      "entities" : entitySchema["entities"],
      "relations" : relationSchema["relations"],
      "equivalences" : equivalenceSchema["equivalences"]
  }
}

entities = [{
                        "ID": "T4",
                        "type": "DNA_Mutation",
                        "begin": "1114",
                        "end": 1122,
                        "text": "mutation"
                    },
                    {
                        "ID": "T6",
                        "type": "DNA_Mutation",
                        "begin": 137,
                        "end": 146,
                        "text": "Mutations"
                    }
]


relations = [
                    {
                        "ID": "R3",
                        "type": "Has_Mutation",
                        "arg1": "T1",
                        "arg2": "T6"
                    },
                    {
                        "ID": "R1",
                        "type": "Has_Mutation",
                        "arg1": "T2",
                        "arg2": "T3"
                    }
                ]


equivalences =  [
                    {
                        "ID": "E0",
                        "type": "alias",
                        "arg1": "T9",
                        "arg2": "T24"
                    },
                    {
                        "ID": "E1",
                        "type": "alias",
                        "arg1": "T1",
                        "arg2": "T20"
                    }
    ]


document = {
    "ID": "21412012",
    "text": "Clinical",
    "entities" : entities,
    "relations" : relations,
    "equivalences":equivalences
}

validate(instance={"entitie" : entities}, schema=entitySchema)
validate(instance={"relations": relations}, schema=relationSchema)
validate(instance={"equivalences":equivalences}, schema=equivalenceSchema)
validate(instance=document, schema=documentSchema)