from jsonschema import validate

schema = {
    "description" : "List of named entities",
    "type": "array",
    "minItems": 0,
    "prefixItems" : {
        "ID" : {"type" : "string"},
        "type" : {"type" : "string"},
        "begin" : {"type" : "number"},
        "end" : {"type" :"number"},
        "text" : {"type" : "string"},
    }
}

validate(instance=[{
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
], schema=schema)