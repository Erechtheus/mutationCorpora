from jsonschema import validate

schema = {
    "description": "An entity",
    "type" : "object",
    "properties" : {
        "ID" : {"type" : "string"},
        "type" : {"type" : "string"},
        "begin" : {"type" : "number"},
        "end" : {"type" :"number"},
        "text" : {"type" : "string"},
    }
}

validate(instance={
                        "ID": "T4",
                        "type": "DNA_Mutation",
                        "begin": 1114,
                        "end": 1122,
                        "text": "mutation"
                    }, schema=schema)