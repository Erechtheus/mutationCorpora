from jsonschema import validate
import json



f = open('code/jsonschema/schema/document.json')
documentSchema = json.load(f)
f.close()

entities = [
    {
        "ID": "T4",
        "type": "DNA_Mutation",
        "begin": 1114,
        "end": 1122,
        "text": "mutation"
    }
]

relations = [
    {
        "ID": "R3",
        "type": "Has_Mutation",
        "arg1": "T1",
        "arg2": "T6"
    }
]

#Regular test
document = {
    "ID": "10205208",
    "text": "Cost comparison of predictive genetic testing versus conventional clinical screening for familial adenomatous polyposis.\n\n\n## BACKGROUND\nMutations of the APC gene cause familial adenomatous polyposis (FAP), a hereditary colorectal cancer predisposition syndrome.\n\n## AIMS\nTo conduct a cost comparison analysis of predictive genetic testing versus conventional clinical screening for individuals at risk of inheriting FAP, using the perspective of a third party payer.\n\n## METHODS\nAll direct health care costs for both screening strategies were measured according to time and motion, and the expected costs evaluated using a decision analysis model.\n\n## RESULTS\nThe baseline analysis predicted that screening a prototype FAP family would cost $4975/ pound3109 by molecular testing and $8031/ pound5019 by clinical screening strategy, when family members were monitored with the same frequency of clinical surveillance (every two to three years). Sensitivity analyses revealed that the genetic testing approach is cost saving for key variables including the kindred size, the age of screening onset, and the cost of mutation identification in a proband. However, if the APC mutation carriers were monitored at an increased (annual) frequency, the cost of the genetic screening strategy increased to $7483/ pound4677 and was especially sensitive to variability in age of onset of screening, family size, and cost of genetic testing of at risk relatives.\n\n## CONCLUSIONS\nIn FAP kindreds, a predictive genetic testing strategy costs less than conventional clinical screening, provided that the frequency of surveillance is identical using either strategy. An additional significant benefit is the elimination of unnecessary colonic examinations for those family members found to be non-carriers.\n",
    "equivalences": [],
    "metadata": [],
    "entities" :  entities,
    "relations" : relations
}

validate(instance=[document],
         schema=documentSchema)

document = {
    "ID": "10205208",
    "text": "Cost comparison of predictive genetic testing versus conventional clinical screening for familial adenomatous polyposis.\n\n\n## BACKGROUND\nMutations of the APC gene cause familial adenomatous polyposis (FAP), a hereditary colorectal cancer predisposition syndrome.\n\n## AIMS\nTo conduct a cost comparison analysis of predictive genetic testing versus conventional clinical screening for individuals at risk of inheriting FAP, using the perspective of a third party payer.\n\n## METHODS\nAll direct health care costs for both screening strategies were measured according to time and motion, and the expected costs evaluated using a decision analysis model.\n\n## RESULTS\nThe baseline analysis predicted that screening a prototype FAP family would cost $4975/ pound3109 by molecular testing and $8031/ pound5019 by clinical screening strategy, when family members were monitored with the same frequency of clinical surveillance (every two to three years). Sensitivity analyses revealed that the genetic testing approach is cost saving for key variables including the kindred size, the age of screening onset, and the cost of mutation identification in a proband. However, if the APC mutation carriers were monitored at an increased (annual) frequency, the cost of the genetic screening strategy increased to $7483/ pound4677 and was especially sensitive to variability in age of onset of screening, family size, and cost of genetic testing of at risk relatives.\n\n## CONCLUSIONS\nIn FAP kindreds, a predictive genetic testing strategy costs less than conventional clinical screening, provided that the frequency of surveillance is identical using either strategy. An additional significant benefit is the elimination of unnecessary colonic examinations for those family members found to be non-carriers.\n",
    "equivalences": [],
    "metadata": [],
    "entities" :  [{"ID": "T4", "type": "DNA_Mutation", "begin": 1114,"end": 1122,"ipsum": "mutation"}],
    "relations" :  []
}

# We dissalow missing entity text
validate(instance=[document],
         schema=documentSchema)


# Check required arguments
#validate(
#    instance={"ID": "10205208"},
#    schema=documentSchema)
