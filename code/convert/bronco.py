import re
import os
import json


inDir = "corpora/original/BRONCO_20151221/"
outFile= "corpora/json/Bronco.json"
inCorpus = inDir +  "BRONCO_FullText_Tabbed_20150602.txt"
inAnnotations = inDir + "BRONCO_MAPPED_final_20151118.txt"


if __name__ == "__main__":
    print("Converting BRONCO corpus to JSON")

#Try to change the working directory to ../../code/ -> needed if called from subdirectory
try:
    os.chdir("../../code/")
except OSError:
    pass


#Parse corpus-file
corpusDict = {}
corpusFile = open(inCorpus, 'r')
for line in corpusFile:
    line = line .strip()
    array = line.split("\t")
    if len(array) != 3:
        print("Error")
    corpusDict[array[0]] = array[1] +"\t" +array[2]