import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from numpy import arange, sin, pi
import math
from statistics import mean 


# with open('scope_9.csv', 'rb') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for row in reader:
#         print ', '.join(row)

fig = plt.figure()


ax = fig.add_subplot(111)

import numpy as np
data = np.genfromtxt('scope_9.csv', delimiter=',', skip_header=1,
                     skip_footer=0, names=['second', 'Ampere'])


# Find all the places where the sign changes, and put them in a list
SignChangeTimeStamps = []
zeroCrossIndexes = []
for i, v in enumerate(data['Ampere']):
    if i == 0:
        change = False
    elif v < 0 and data['Ampere'][i-1] > 0:
        change = True
        # print "true"
        SignChangeTimeStamps.append(data['second'][i-1])
        zeroCrossIndexes.append(i-1)
    elif v > 0 and data['Ampere'][i-1] < 0:
        change = True
        # print "true"
        SignChangeTimeStamps.append(data['second'][i-1])
        zeroCrossIndexes.append(i-1)
    else:
        change = False


# We assume that there are 3 zero crossings in the data set, and use this to determine the cycle time by averaging the delta and multiplying it by 2
# Shift it over by the first zero crossing times negative one, so that the first zero crossing is at x=0. Also record min/max values
timeToShiftBy = SignChangeTimeStamps[0] * -1
i = 0
min = 0
max = 0
tmin = 0
tmax = 0
extrimaIndex = [0,0]

for x in np.nditer(data):
    dautum = data['second'][i]
    dautum += timeToShiftBy
    data['second'][i] = dautum
    if data['Ampere'][i] > max:
        max = data['Ampere'][i]
        tmax = data['second'][i]
        extrimaIndex[1] = i
    if data['Ampere'][i] < min:
        min = data['Ampere'][i]
        tmin = data['second'][i]
        extrimaIndex[0] = i
    i += 1

# Also shift the sign change time stamps
i=0
for indecies in SignChangeTimeStamps:
    i += 1
    SignChangeTimeStamps[i-1] += timeToShiftBy


# Derive the average frequency, magnitude and initial slope (and make the slope negative if necessary)
averageFrequecy = ((SignChangeTimeStamps[2] - SignChangeTimeStamps[1]) + (SignChangeTimeStamps[1] - SignChangeTimeStamps[0]) )
averageMagnitude = (abs(min) + abs(max))/2
initialSlope = data['Ampere'][15] - data['Ampere'][5]
# print initialSlope
if initialSlope < 0:
    averageMagnitude = averageMagnitude * -1


# Try to make a array with the optimal sine wave in it
optimalSineWave = []
deviation = []
percentDeviation = []
percentDeviationSquared = []
translatedSineWave = []
for x in range(np.size(data)):
    optimalSineWave.append(averageMagnitude * sin(2 * 3.1415926 * data['second'][x] / averageFrequecy ))
    # deviation.append(abs(optimalSineWave[x] - data['Ampere'][x]))
    translatedSineWave.append(optimalSineWave[x] + averageMagnitude )
    deviation.append(abs(translatedSineWave[x] - (data['Ampere'][x] + averageMagnitude) ) )
    percentDeviation.append(deviation[x]/translatedSineWave[x])


print("Non-Linearity: % s%%" % (abs(mean(percentDeviation) ) ) )


# print extrimaIndex, zeroCrossIndexes
quarterWave1 = []#np.zeros((extrimaIndex[0] - zeroCrossIndexes[0], 2))
quarterWave2 = []#np.zeros((zeroCrossIndexes[1] - extrimaIndex[0], 2))
quarterWave3 = []#np.zeros((extrimaIndex[1] - zeroCrossIndexes[1], 2))
quarterWave4 = []#np.zeros((zeroCrossIndexes[2] - extrimaIndex[1], 2))
wave1time = []
wave2time = []
wave3time = []
wave4time = []

# Make a list of half waves one and three, which don't need to be reflected/transformed
for x in range( extrimaIndex[0] - zeroCrossIndexes[0] ):
    quarterWave1.append(abs(data['Ampere'][x+zeroCrossIndexes[0]]))
    wave1time.append(data['second'][x+zeroCrossIndexes[0]])
for x in range( zeroCrossIndexes[1] - extrimaIndex[0] ):
    quarterWave2.append(abs(data['Ampere'][zeroCrossIndexes[1]-x]))
    wave2time.append(data['second'][x+extrimaIndex[0]])
for x in range( extrimaIndex[1] - zeroCrossIndexes[1] ):
    quarterWave3.append(abs(data['Ampere'][x+zeroCrossIndexes[1]]))
    wave3time.append(data['second'][x+zeroCrossIndexes[1]])
for x in range( zeroCrossIndexes[2] - extrimaIndex[1] ):
    quarterWave4.append(abs(data['Ampere'][zeroCrossIndexes[2]-x]))
    wave4time.append(data['second'][x+extrimaIndex[1]])

# This is such a hack
minlen = len(wave1time)
if len(wave2time) > minlen:
    minlen = len(wave2time)
if len(wave3time) > minlen:
    minlen = len(wave3time)
if len(wave4time) > minlen:
    minlen = len(wave4time)


percentDeltas = []
for x in range( minlen ):
    datas = [quarterWave1[x], quarterWave2[x], quarterWave3[x], quarterWave4[x]]
    print datas
    print min(datas)
    # percentDeltas[x] = (max(datas) - min(datas))#/data['Ampere'][x]
# print("Mean wave delta: % s%%" % (abs(mean(percentDeviation) ) ) )





# plot the stuff
# ax.plot(data['second'], optimalSineWave, linewidth=3, color='c')
# ax.plot(data['second'], data['Ampere'], color='k', label='the data')
ax.axhline(linewidth=1, color='k')
ax.plot(data['second'], deviation, linewidth=1.5, color='r')
ax.plot(wave1time, quarterWave1)#, linewidth=1.5, color='r')
ax.plot(wave2time, quarterWave2)#, linewidth=1.5, color='r')
ax.plot(wave3time, quarterWave3)#, linewidth=1.5, color='r')
ax.plot(wave4time, quarterWave4)#, linewidth=1.5, color='r')

# i=0
for x in range(len(SignChangeTimeStamps)):
    # i+=1
    ax.axvline(x=SignChangeTimeStamps[x-1], color='g')
ax.axvline(x=tmin, color='b')
ax.axvline(x=tmax, color='b')

ax.set_title("Current vs time")
ax.set_xlabel("Time in seconds")
ax.set_ylabel("Current in amperes")


plt.show()