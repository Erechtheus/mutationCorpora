import random
import json
import os
from pathlib import Path

randomSeed = 1202
splitSize = 80 / 100
inFolder="../../corpora/json/"
outFOlder="splits/"

if __name__ == "__main__":
    print("Generate train/test splits for corpora without dedicated train/test-splits")

#Create export-directories if necessary
if os.path.isdir(outFOlder) == False:
    os.makedirs(outFOlder )


for path in Path(inFolder).glob('*.json'):

    folderName = os.path.basename(path)
    folderName = folderName[:-5]

    #Skip corpora with dedicated train/test splits (e.g., AMIA or tmvar)
    if "train" in folderName or "test" in folderName:
        continue

    print(path)

    with open(path) as f:
        corpus = json.load(f)
    f.close()

    allIDs = sorted(list(set(map(lambda x :x["document"]["ID"], corpus["documents"]))))

    random.Random(randomSeed).shuffle(allIDs)

    trainIDs = allIDs[0:int(len(allIDs) * splitSize)]
    testIDs = allIDs[int(len(allIDs) * splitSize):]

    if len(allIDs) != len(trainIDs) + len(testIDs):
        print("Error!")


    outputDict = {}
    outputDict["corpus"] = folderName
    outputDict["seed"] = randomSeed
    outputDict["trainIDs"] = trainIDs
    outputDict["testIDs"] = testIDs

    f = open(outFOlder +folderName +".json", "w")
    f.write(json.dumps(outputDict, indent=4))
    f.close()
