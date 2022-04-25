from re import A
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

easymini = pd.read_csv("D:\\Documents\\AltusMetrum\\super guppy easymini 6363.csv")
easymini2 = pd.read_csv("D:\\Documents\\AltusMetrum\\super guppy easymini 6357.csv")
fcb = pd.read_csv("D:\\Downloads\\v1super-guppy-4-23-output-post.csv")
ground = pd.read_csv("D:\\Documents\\Github\\pyqt_groundstation\\export.csv")
# print(easymini)
print(ground.keys())
fcb['timestamp_s'] = fcb['timestamp_s'] / 1000 - 209.1
plt.figure()

# plt.subplot(211)
plt.scatter(fcb['timestamp_s'], fcb['baro2_pres'] * 101325, label="FCB Baro 2 (pa)")
plt.scatter(easymini['time'], easymini['pressure'], label="Easymini (pa)")
plt.scatter(easymini2['time'], easymini2['pressure'], label="Easymini 2 (pa)")
plt.legend()

# plt.subplot(212)
# plt.plot(fcb['timestamp_s'], fcb['pos_z'], label="FCB alt (m)")
# plt.plot(fcb['timestamp_s'], fcb[''], label="FCB alt (m)")
# plt.plot(fcb['timestamp_s'], -fcb['imu1_accel_x_real'], label="FCB vertical accel (m)")
# plt.plot(easymini['time'], easymini['altitude'] - easymini['altitude'][0], label="Easymini 1 (m)")
# plt.plot(easymini2['time'], easymini2['altitude'] - easymini2['altitude'][0], label="Easymini 2 (m)")

plt.legend()
plt.show()