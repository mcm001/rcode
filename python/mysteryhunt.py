from calendar import firstweekday
import pandas
import numpy as np

# left = ['dash','pie','pink','union']
# right = ['cam','charts','sparkle','jack']
# idx = np.array([2,4,5,2]) - 1

left = ["BEARD", "DONKEY", "GABLE", "TRAFFIC"]
right = ["GRASS", "FOAL", "ROOF", "CONES"]
idx = np.array([1,4,4,1]) - 1

# start from the first word, then try all of them
for firstWordIdx in range(4):
    for secondWordIdx in range(4):
        for thirdWordIdx in range(4):
            for fourthWordIdx in range(4):
                list = [firstWordIdx, secondWordIdx, thirdWordIdx, fourthWordIdx]
                if len(list) != len(set(list)):
                    continue

                # We now have a unique set of indexes

                word1 = right[firstWordIdx]
                word2 = left[secondWordIdx]
                word3 = left[thirdWordIdx]
                word4 = right[fourthWordIdx]

                try:
                    print(f"{word1[idx[0]]}{word2[idx[1]]}{word3[idx[2]]}{word4[idx[3]]}")
                except Exception as e:
                    # print(f"{word1} {word2} {word3} {word4}")
                    pass
                
