from jsonschema import validate

entitiesSchema = {
        "description" : "List of named entities",
        "type": "array",
        "items" : {
            "type" : "object",
            "properties": {

                "ID" : {"type" : "string"},
                "type" : {"type" : "string"},
                "begin" : {"type" : "number"},
                "end" : {"type" :"number"},
                "text" : {"type" : "string"}
            },
            "required": [
                "ID", "type", "begin", "end", "text"
            ]
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

validate(instance=entities, schema=entitiesSchema)

