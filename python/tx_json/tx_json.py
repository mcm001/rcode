import numpy as np
import json
import os

outputFile = open("output.csv", "w")

directory = "D:\Downloads\TX_Anderson_48001_LTE_JSON_04052021~1"
for filename in os.listdir(directory):
    with open(directory + "/" + filename) as f:
        data = json.load(f)
        for row in data:
            if "Mobile Info" in row:
                info = row["Mobile Info"]
                android = info["Android"]
                temp = android["CPU Temperature"]

                outputFile.write(temp)
                outputFile.write("\n")

                try:
                    t = int(temp)
                except ValueError:
                    print("Cannot convert {} to int".format(temp))

outputFile.flush()
outputFile.close()