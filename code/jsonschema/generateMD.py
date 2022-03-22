import json
import jsonschema2md

parser = jsonschema2md.Parser(
    examples_as_yaml=False,
    show_examples="all",
)
with open("code/jsonschema/entities.json", "r") as json_file:
    md_lines = parser.parse_schema(json.load(json_file))
print(''.join(md_lines))