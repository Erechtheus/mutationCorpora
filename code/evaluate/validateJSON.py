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
            "text" : {"type" : "string"},
        }
    }
}
entities = [{
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

#validate(instance=entities, schema=schema)
validate(instance={"entities" : entities}, schema=entitySchema)