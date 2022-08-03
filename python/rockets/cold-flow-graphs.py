import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

data = pd.read_csv("D:\\Documents\\GitHub\\pyqt_groundstation\\logs\\07-24-2022_09-29-13\\PROP_DATA_0.txt")
other = open("D:\\Documents\\GitHub\\pyqt_groundstation\\logs\\07-24-2022_09-29-13\\PROP_OTHER_MSGS.txt").readlines()

transitions = []
for line in other:
    if line.startswith("NON-DATA"):
        line = line.split(" : ")[2] #extract json
        line = json.loads(line)
        print(line)

        transitions.append(line["timeStamp"])

times = (min(transitions) - 50000, max(transitions))

plt.figure()       
plt.subplot(311)
plt.plot(data["timeStamp"], data["tank1Thermo"], label="tank 1 thermo")
[plt.axvline(t, color="r") for t in transitions]
plt.xlim(times)
plt.legend()

plt.subplot(312)
plt.plot(data["timeStamp"], data["loxTankDucer"], label="lox tank, psi")
plt.plot(data["timeStamp"], data["loxVenturi"], label="lox venturi, psi")
# plt.plot(data["timeStamp"], data["loxRegDucer"], label="lox reg, psi")
[plt.axvline(t, color="r") for t in transitions]
plt.xlim(times)
plt.legend()

valveNames = "kerDrip	kerFlow	kerPressurant	kerPurge	kerVent	loxDrip	loxFlow	loxPressurant	loxPurge	loxVent".split("	")
plt.subplot(313)
for v in valveNames:
    series = data[v].apply(lambda x: 1 if x == "OPEN" else 0)
    plt.plot(data["timeStamp"], series, label=v)
plt.legend()
plt.xlim(times)

plt.show()
