import serial
import serial.tools.list_ports


import pandas as pd
csv = pd.read_csv("D:\\Documents\\GitHub\\dpf-line-cutter\\code\\launch archive\\2021-08-21 StAlbans\\2021-08-21_TRDCherryLineCutterFlashData")

import numpy as np
csv = np.array(csv)
pressure = csv[:, 2]
pressure = pressure[108500:111200]
print(pressure.shape)

with open("out.csv", 'w') as f:
    for p in pressure:
        f.write(f"{int(p)}")
        f.write(",")

# np.savetxt("out.csv", pressure, delimiter=',', fmt="%f")

import matplotlib.pyplot as plt
plt.figure()
plt.plot(pressure)
plt.show()

ports = serial.tools.list_ports.comports(include_links=False)
port = None
for port in ports :
    print('Found device at port '+ port.device)
if ports == [] or port is None:
    print("No devices found!")
ser = serial.Serial(port.device)
if ser.isOpen():
    ser.close()
ser = serial.Serial(port.device, 9600, timeout=1)
ser.flushInput()
ser.flushOutput()
print('Connected to ' + ser.name)
