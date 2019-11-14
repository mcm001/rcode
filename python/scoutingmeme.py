import numpy

print("======================welcome======================\n")

slots = 2 # int(input("How many scouters per alliance station? "))
numScouters = 15 # int(input("How many scouters? "))
periods = 2 #int(input("How many periods? "))
numBreak = 0

scouters = []
s=0
while(s<numScouters):
  scouters.append(s)
  s+=1

print("scouters %s" % scouters)

if(numScouters >= slots*6):
  numBreak = numScouters-(6*slots)
  print(numBreak)
else:
  print("Not enough scouters")

onBreak = [x[:] for x in [[-1] * numBreak] * periods]
scouting = [x[:] for x in [[[-1] * slots] * 6] * periods]

print("scouting %s\n" % scouting)

bottomOfTheStack = numScouters - 2

rotIndex=0

k=0
while(rotIndex<periods): # make a schedule for every rotation
  j=0
  j2 = 0
  nxt=0
  while(j<6): # loop over each alliance station
    print(scouting[rotIndex][j])
    slotNum=0
    while(slotNum<slots):
      print(scouters[nxt+slotNum])
      # scouting[rotIndex][j].insert(slotNum, scouters[nxt+slotNum])
      # scouting[rotIndex][j].pop(slotNum+1)
      scouting[rotIndex][j][slotNum] = scouters[nxt+slotNum]
      print(scouting[rotIndex][j][slotNum])
      # print(scouting[rotIndex][j])
      slotNum+=1
    print(scouting[rotIndex][j])
    print(scouting[rotIndex][3])
    nxt+=slots
    print(scouting[rotIndex])
    # print(nxt)
    j = j+1

  print("\n")
  print("Scouting in the %s th period is %s " % (rotIndex, scouting[rotIndex]))
  print()

  while(j2<numBreak):
    onBreak[rotIndex][j2] = scouters[bottomOfTheStack-j2]
    j2+=1
  bottomOfTheStack -=1
  rotIndex+=1
      

print(onBreak)
print(scouting)