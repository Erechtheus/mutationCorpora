from jsonschema import validate
import json

f = open('code/jsonschema/relations.json')
newSchema = json.load(f)
f.close()

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





#We allow empty entities array
validate(instance=[], schema=newSchema)
#We allow filled entities array
validate(instance=relations, schema=newSchema)

#We dissalow missing type
validate(instance = [{"ID": "R3", "lorum": "Has_Mutation", "arg1": "T1", "arg2": "T6"}], schema=newSchema)


#We require relations as input
#validate(instance = {}, schema=newSchema)
