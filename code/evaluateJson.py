import json

inFile="corpora/json/amia-test.json"
inFile="corpora/json/amia-train.json"
inFile="corpora/json/Nagel.json" #Error!
inFile="corpora/json/linking/osiris.json" #Error!
inFile="corpora/json/SETH.json"
inFile="corpora/json/linking/thomas.json" #Error!
inFile="corpora/json/tmvar-test.json"
inFile="corpora/json/tmvar-train.json"
inFile="corpora/json/linking/tmvarnorm.json"
inFile="corpora/json/Variome.json"

with open(inFile) as f:
    documents = json.load(f)
    for document in documents["documents"]:

        document = document["document"]

        id = document["ID"]
        text = document["text"]
        entities = document["entities"]
        relations = document["relations"]

        #if document.keys() not in ['ID', 'text', 'entities', 'relations', 'metadata']:
        #    print("unknown key" +str(document.keys()))


        for entity in entities:
            if text[entity["begin"] : entity["end"]] != entity["text"]:
                print("Problem with document '" +str(id) +"' entity offset wrong for '" +entity["text"] +"' != '" +text[entity["begin"] : entity["end"]] +"'")
                print(entity)
                print("---")

        for relation in relations:

            relId = relation["ID"]
            relType = relation["type"]
            relArg1 = relation["arg1"]
            relArg2 = relation["arg2"]

            arg1 = list(filter(lambda x: x["ID"] == relArg1, entities))
            arg2 = list(filter(lambda x: x["ID"] == relArg2, entities))

            if (len(arg1) != 1):
                print("Problem with document '" +str(id) +"' number of relations wrong for relation= " +str(relation))


f.close()