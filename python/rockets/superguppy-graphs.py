import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

easymini = pd.read_csv("D:\\Documents\\AltusMetrum\\beanboozler easymini 8069.csv")
fcb = pd.read_csv("D:\\Documents\\GitHub\\python-avionics\\output\\beanboozler-4-24-2022-output-post.csv")
# print(easymini)
print(fcb.keys())
fcb['timestamp_s'] = fcb['timestamp_s'] / 1000 - 355
plt.figure()
plt.scatter(easymini['time'], easymini['pressure'], label="Easymini (pa)")
plt.scatter(fcb['timestamp_s'], fcb['baro1_pres'] * 101325, label="FCB Baro 1 (pa)")
plt.scatter(fcb['timestamp_s'], fcb['baro2_pres'] * 101325, label="FCB Baro 2 (pa)")
# plt.plot(fcb['timestamp_s'], fcb['imu1_accel_y_real'], label="FCB ax")
plt.legend()
plt.show()