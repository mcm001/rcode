import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# easymini = pd.read_csv("D:\\Documents\\AltusMetrum\\beanboozler easymini 8069.csv")
fcb = pd.read_csv("D:\\Documents\\GitHub\\python-avionics\\output\\beanboozler-4-24-2022-output-post.csv")
ork = pd.read_csv("D:\\Documents\\GrabCAD\\Cert Rocket\\Intimidator 2.6\\i140-sim.csv")

print(fcb)
print(ork)
fcb['timestamp_s'] = fcb['timestamp_s'] / 1000 - 353.8
plt.figure()
# plt.plot(easymini['time'], easymini['pressure'], label="Easymini (pa)")
# plt.plot(fcb['timestamp_s'], fcb['baro1_pres'] * 101325, label="FCB Baro 1 (pa)")
# plt.plot(fcb['timestamp_s'], fcb['baro2_pres'] * 101325, label="FCB Baro 2 (pa)")

plt.plot(fcb['timestamp_s'], fcb['imu1_accel_y_real'] - 9.81, label="FCB ax, m/s/s")
plt.plot(pd.to_numeric(ork['Time']), ork['Accel'] * 9.81, label="OpenRocket Accel, m/s/s")

plt.ylim((-10, 80))
plt.xlim((-2, 15))

plt.legend()
plt.show()