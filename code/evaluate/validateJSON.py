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

entities = { "entities" :
    [{
                        "ID": "T4",
                        "type": "DNA_Mutation",
                        "begin": 1114,
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
}

relations = {
"relations": [
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
}

equivalences = {
"equivalences": [
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
}

validate(instance=entities, schema=entitySchema)
validate(instance=relations, schema=relationSchema)
validate(instance=equivalences, schema=equivalenceSchema)
