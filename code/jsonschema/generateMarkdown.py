import glob
import json
import jsonschema2md
from pathlib import Path

parser = jsonschema2md.Parser(
    examples_as_yaml=False,
    show_examples="all",
)

for file in glob.glob("code/jsonschema/schema/*.json"):
    filename = Path(file).stem
    #print(filename)

    with open(file, "r") as json_file:
        md_lines = parser.parse_schema(json.load(json_file))

    with open("code/jsonschema/markdown/" +filename +".md", 'w') as f:
        f.write(''.join(md_lines))
    f.close()

    #print(''.join(md_lines))