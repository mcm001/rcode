import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir="D:\\Documents\\GitHub\\dpf-line-cutter\\code\\launch archive\\2021-10-24 StAlbansMarman")
csv = pd.read_csv(file_path)

csv = np.array(csv)
pressure = csv[:, 2]
pressure = np.append(pressure[0:12000],pressure[140000:150000])
plt.figure()
plt.plot(pressure)
plt.show()
# pressure = 44330.76 * (1.0 - pow(pressure / 101451, 1.0 / 5.25588))
# pressure = pressure[108500:111200]
print(pressure.shape)

# with open("D:\\Documents\\GitHub\\dpf-line-cutter\\code\\v3\\line_cutter_v3\\simdata.h", 'w') as f:
with open("out.csv", 'w') as f:
    f.write(f"int p[{len(pressure)}]=" + '{')
    for p in pressure:
        f.write(f"{int(p)}")
        f.write(",")
    f.write("};")

# np.savetxt("out.csv", pressure, delimiter=',', fmt="%f")

# plt.figure()
# plt.plot(pressure)
# plt.show()

# ports = serial.tools.list_ports.comports(include_links=False)
# port = None
# for port in ports :
#     print('Found device at port '+ port.device)
# if ports == [] or port is None:
#     print("No devices found!")
# ser = serial.Serial(port.device)
# if ser.isOpen():
#     ser.close()
# ser = serial.Serial(port.device, 9600, timeout=1)
# ser.flushInput()
# ser.flushOutput()
# print('Connected to ' + ser.name)
