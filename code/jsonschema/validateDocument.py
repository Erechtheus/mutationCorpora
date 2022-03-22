from jsonschema import validate


documentSchema = {
    "title": "Document",
    "description": "A simple document",
    "type": "object",
    "properties": {
        "ID": {"type": "string"},
        "text": {"type": "string"},
        "entities": {
            "$ref": "file:code/jsonschema/entities.json"
        }
        #      "relations" :
        #      "metadata"
    },
    "required": [
        "ID",
        "text",
        "entities"
    ]
}

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

document = {
    "ID": "10205208",
    "text": "Cost comparison of predictive genetic testing versus conventional clinical screening for familial adenomatous polyposis.\n\n\n## BACKGROUND\nMutations of the APC gene cause familial adenomatous polyposis (FAP), a hereditary colorectal cancer predisposition syndrome.\n\n## AIMS\nTo conduct a cost comparison analysis of predictive genetic testing versus conventional clinical screening for individuals at risk of inheriting FAP, using the perspective of a third party payer.\n\n## METHODS\nAll direct health care costs for both screening strategies were measured according to time and motion, and the expected costs evaluated using a decision analysis model.\n\n## RESULTS\nThe baseline analysis predicted that screening a prototype FAP family would cost $4975/ pound3109 by molecular testing and $8031/ pound5019 by clinical screening strategy, when family members were monitored with the same frequency of clinical surveillance (every two to three years). Sensitivity analyses revealed that the genetic testing approach is cost saving for key variables including the kindred size, the age of screening onset, and the cost of mutation identification in a proband. However, if the APC mutation carriers were monitored at an increased (annual) frequency, the cost of the genetic screening strategy increased to $7483/ pound4677 and was especially sensitive to variability in age of onset of screening, family size, and cost of genetic testing of at risk relatives.\n\n## CONCLUSIONS\nIn FAP kindreds, a predictive genetic testing strategy costs less than conventional clinical screening, provided that the frequency of surveillance is identical using either strategy. An additional significant benefit is the elimination of unnecessary colonic examinations for those family members found to be non-carriers.\n",
    "equivalences": [],
    "metadata": [],
    "entities" : {"entities" : entities}
}

# We dissalow missing text
validate(instance=document,
         schema=documentSchema)

# Check required arguments
#validate(
#    instance={"ID": "10205208"},
#    schema=documentSchema)
