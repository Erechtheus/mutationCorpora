from jsonschema import validate
import json

f = open('code/jsonschema/entities.json')
newSchema = json.load(f)
f.close()


entities = [
    {
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




#We allow empty entities array
validate(instance={"entities": []}, schema=newSchema)
#We allow filled entities array
validate(instance={"entities": entities}, schema=newSchema)

#We dissalow missing text
validate(instance = {"entities" : [{"ID": "T4", "type": "DNA_Mutation", "begin": 1114,"end": 1122,"ipsum": "mutation"}]}, schema=newSchema)

#We dissalow wrong type (i.e. string instread of integer)
validate(instance = {"entities" : [{"ID": "T4", "type": "DNA_Mutation", "begin": "1114","end": 1122,"text": "mutation"}]}, schema=newSchema)

#We require entities as input
validate(instance = {}, schema=newSchema)
