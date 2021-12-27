from math import acos
from time import time
from ahrs.common.constants import M_PI, RAD2DEG
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import frccontrol as fct
import control as ct
from frccontrol import kalmd

altArr = None
dt = None
timeArr = None

def make_goose():
    # in this dataset, ay is up
    global timeArr, altArr, dt, ayArr, temperature, csv
    # csv = pd.read_csv("D:\\Documents\\Angry Goose TCC 5-15-21.txt")
    # csv = pd.read_csv("D:\\Documents\\Angry Goose StAlbans 11-20-21.txt")
    csv = pd.read_csv("D:\\Documents\\pendulum test 2.txt")
    timeArr = csv['time']
    timeArr = timeArr / 1000
    timeArr = timeArr

    # Convert to mpss sans earth gravity
    ayArr = -csv['ay']
    # ayArr = ayArr - 1
    # ayArr = ayArr * 9.81

    # ayArr = csv['ay']**2+csv['ax']**2+csv['az']**2
    # ayArr=np.sqrt(ayArr)

    ayArr = ayArr - 1
    ayArr = ayArr * 9.81

    # Already in meters
    altArr = csv['alt']

    temperature = csv['temp'] / 100 # cenit-celcius to C
 
    # dt = 50/1000 # ms
    dt = np.mean(np.diff(timeArr))

def make_drone_goose():
    # in this dataset, ay is up
    global timeArr, altArr, dt, ayArr
    csv = pd.read_csv("D:\\Documents\\drone test 2 12-11021.txt")
    timeArr = csv['time']
    timeArr = timeArr / 1000
    # timeArr = timeArr - 670

    # Convert to mpss sans earth gravity
    # ayArr = csv['ay']
    # ayArr = ayArr - 1
    # ayArr = ayArr * 9.81
    ayArr = csv['ay']**2+csv['ax']**2+csv['az']**2
    ayArr=np.sqrt(ayArr)
    ayArr = ayArr - 1
    ayArr = ayArr * 9.81

    # Already in meters
    altArr = csv['altitude']

    dt = 21/1000 # ms

def make_fcb(num = 3):
    global timeArr, altArr, dt, ayArr, csv
    if num == 1:
        df = pd.read_csv("D:\\Downloads\\output-post.csv")
    elif num == 2:
        df = pd.read_csv("D:\\Downloads\\fcb-06-20-2021-output-post(1).csv")
    elif num == 3:
        df = pd.read_csv("D:\\Downloads\\fcb-mdra-marmon-12-19-2021.csv")
    elif num == 4:
        df = pd.read_csv("D:\\Downloads\\magcal_raw.csv")
    csv = df
    # print(csv)
    timeArr = df["timestamp_s"] / 1000
    ayArr = np.abs(df["imu_accel_y_avg"]) - 9.81
    # ayArr = df['imu_accel_x_avg']**2+df['imu_accel_y_avg']**2+df['imu_accel_z_avg']**2
    # ayArr=np.sqrt(ayArr)
    # ayArr = ayArr - 9.81
    altArr = (df["baro_temp_avg"] / -0.0065) * (1 - pow(df["baro_pres_avg"] / df["baro_pres_avg"][0], 287.0474909 * -0.0065 / 9.80665)) * 10

    # dt = np.mean(np.diff(timeArr))
    dt = .0155 # On average, during flight 

    return csv

def make_line_cutter():
    global timeArr, altArr, dt, ayArr
    df = pd.read_csv("D:\\Documents\\GitHub\\dpf-line-cutter\\code\\launch archive\\2021-11-14 MDRA\\Cherry_flight_data.csv",
        names=['state', 'time', 'pressure', 'altitude','avalt','delta-alt','av-delta-alt', 'temp','ax','ay','az','battsense','cutsense1','cutsense2','currentsense','photores'])
    # df = pd.read_csv("D:\\Downloads\\fcb-06-20-2021-output-post(1).csv")
    timeArr = df["time"] / 1000
    ayArr = (df["ax"]**2+df['ay']**2+df['az']**2)**0.5 * 9.81 - 9.81
    # altArr = (df["baro_temp_avg"] / -0.0065) * (1 - pow(df["baro_pres_avg"] / df["baro_pres_avg"][0], 287.0474909 * -0.0065 / 9.80665)) * 10
    altArr = 44330.76 * (1.0 - (df['pressure'] / 101295)**(1.0 / 5.25588))
    dt = np.mean(np.diff(timeArr))

# Our system state is [pos, vel]
# inputs are [accel]
# outputs are [pos]
# https://www.wolframalpha.com/input/?i=%28%7B%7B0%2C1%7D%2C%7B0%2C0%7D%7D+dot+%7B%7B2%7D%2C+%7B1%7D%7D+%29%2B+%28+%7B%7B0%7D%2C%7B1%7D%7D+dot+%7B3%7D%29
# x-dot = [vel  ] = [0 1] * [pos] + [0] * [accel]
#         [accel]   [0 0]   [vel]   [1] 
# y = [pos] = [1 0] * [pos] + [0] * [accel]
#                     [vel]

def make_cov_matrix(elems):
    return np.diag(np.square(elems))

def do_kalman():
    global uArray, buarray, xhatarr
    global timeArr, altArr, dt, ayArr, xhatarr
    global stateArray
    global apogeeTime
    apogeeTime = 0

    sysc = ct.ss(np.array([[0,1],[0,0]]), np.array([[0],[1]]), np.array([1,0]), np.array([0]))
    sysd = sysc.sample(dt)  # Discretize model
    # sysd = ct.ss(np.array([[1, dt, dt* dt /2],[0,1, dt],[0,0,1]]), np.array([[0,0],[0,0],[0,0]]), np.array([[1,0,0],[0,0,1]]), np.array([[0, 0], [0, 0]]))
    print(sysd)

    # Q is our process noise covariance
    # It's [pos variance, vel variance, accel variance]^t
    # R is measurement noise (how sure we are about out measurement)
    Q = make_cov_matrix([0.5, 1])
    R = make_cov_matrix([50])

    kalman_gain, P_steady = kalmd(sysd, Q, R)
    # kalman_gain = np.array([[.01657], [.0934]])
    print(kalman_gain)

    # We assume we start at 0 position and velocity
    xhatarr = []
    x_hat = np.array([[0], [0]])

    uArray = []
    buarray  = []
    last_alt = 0
    state = 0
    stateArray = []

    for (t, accel, altitude) in zip(timeArr, ayArr, altArr):
        if state >= 2:
            u = np.array([[0]])
        else:
            u = np.array([[accel]])

        # uArray.append(u[0,0])
        # bu = np.dot(sysd.B, u)
        # buarray.append([bu[0,0], bu[1,0]])
        # u = np.array([[0],[0]])
        # y = np.array([[altitude], [accel]])

        y = np.array([[altitude]])
        
        # predict
        x_hat = sysd.A @ x_hat + sysd.B @ u

        # correct
        x_hat += kalman_gain @ (
            y - sysd.C @ x_hat - sysd.D @ u
        )

        xhatarr.append([x_hat[0,0], x_hat[1,0]])

        if x_hat[0,0] > 50 and state == 0:
            state = 1 # boost 
        elif state == 1 and last_alt > x_hat[0,0] and x_hat[1,] < 0:
            apogeeTime = t
            state = 2 # apogee


        last_alt = x_hat[0,0]
        stateArray.append(state)

    # Convert to NP array so we can slice
    xhatarr = np.array(xhatarr)
    buarray = np.array(buarray)

import json
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def do_gyro_integration(mag_data):
    global csv, timeArr, orientation, dt
    import ahrs.filters as filters
    import ahrs.common.orientation as orient

    if "wx_raw" in csv:
        gyro_data = np.array([csv["wx_raw"] / 32.8,csv["wy_raw"] / 32.8, csv["wz_raw"] / 32.8]).T
        gyro_data = gyro_data * M_PI / 180.0 # deg/s to rad/s
    elif "imu1_gyro_x_real" in csv:
        gyro_data = np.array([csv["imu1_gyro_x_real"],csv["imu1_gyro_y_real"], csv["imu1_gyro_z_real"]]).T
    else:
        gyro_data = np.array([csv["wx"],csv["wy"], csv["wz"]]).T
        gyro_data = gyro_data * M_PI / 180.0 # deg/s to rad/s

    # Crappy gyro cal -- subtract out the average of the first 10
    gyro_offset = [np.mean(gyro_data[:100,0]), np.mean(gyro_data[:100,1]), np.mean(gyro_data[:100,2])]
    gyro_data = gyro_data - gyro_offset

    if "ax" in csv:
        acc_data = np.array([csv["ax"] * 9.81,csv["ay"] * 9.81,csv["az"] * 9.81]).T
    else:
        acc_data = np.array([csv["imu1_accel_x_real"],csv["imu1_accel_y_real"],csv["imu1_accel_z_real"]]).T
    
    # gyro_data = gyro_data[900:,:]
    # initial_tilt = orient.acc2q(acc_data[900,:])
    initial_tilt = orient.ecompass(acc_data[0], mag_data[0], frame='ENU', representation='quaternion')

    rotM = orient.q2R(initial_tilt)
    newX = np.array([1,0,0]).T @ rotM
    angleBetween = newX @ np.array([1,0,0]).T
    print(f"Initial tilt: {initial_tilt} angle {acos(angleBetween) * RAD2DEG}")

    # orientation = filters.Mahony(gyr=gyro_data, acc=acc_data, frequency=1.0/np.mean(np.diff(timeArr)))
    # orientation = filters.Tilt(acc=acc_data)
    orientation = filters.AngularRate(gyr=gyro_data[1000:,:], q0=initial_tilt, frequency=1/dt)
    
    import RocketEKF
    from ahrs.utils.wmm import WMM
    # MDRA
    wmm = WMM(latitude=39.0785319, longitude=-75.87425944, height=0)

    # X is north, Y  is East, Z is down
    # So by default, it's NED
    # We want East-North-Up
    m_ref = np.array([wmm.Y, wmm.X, -wmm.Z]) / 1000
    print(f"Mag ref: {m_ref} microTesla")
    # o2 = RocketEKF.EKF(gyr=gyro_data, mag=mag_data, frequency=1/np.mean(np.diff(timeArr)), q0=initial_tilt, m_ref=m_ref, frame='ENU')
    # orientation = o2

    # np.savetxt('orient.mat', json.dumps(orientation.Q.tolist())
    json_dump = json.dumps(orientation.Q, 
                       cls=NumpyEncoder)
    # print(json_dump)
    with open("orient.json", "w") as txt:
        txt.write(json_dump)


def plot_gyro():
    global csv, timeArr, orientation
    import ahrs.common.orientation as orient

    euler = []
    for row in orientation.Q:
        # Roll is about x, pitch about y and yaw is about z
        # The coordinate system appears to be NED (North-East-Down)??
        # I know for sure Z axis is vertical
        euler.append(orient.q2rpy(row))
    euler = np.array(euler)
    euler = euler * RAD2DEG
    plt.figure()
    plt.subplot(211)
    # plt.plot(timeArr, euler[:,0], label="Roll, deg")
    # plt.plot(timeArr, euler[:,1], label="Pitch, deg")
    # plt.plot(timeArr, euler[:,2], label="Yaw, deg")
    plt.plot(euler[:,0], label="Roll, deg")
    plt.plot(euler[:,1], label="Pitch, deg")
    plt.plot(euler[:,2], label="Yaw, deg")
    plt.plot(csv["imu1_accel_y_real"], label="Yaw, deg")
    plt.plot(csv["pos_z"], label="Yaw, deg")
    plt.legend()
    plt.subplot(212)
    # plt.plot(timeArr, csv['ax'], label="Ax, gees")
    # plt.plot(timeArr, csv['ay'], label="Ay, gees")
    # plt.plot(timeArr, csv['az'], label="Az, gees")
    plt.legend()

def rotation_matrix(quat):
    import math
    w, x, y, z = quat
    norm = math.sqrt(w ** 2 + x ** 2 + y ** 2 + z ** 2)
    if norm == 1:
         s = 2.0
    elif norm > 0:
        s = 2.0 / norm
    else:
        s = 0

    xs = x * s
    ys = y * s
    zs = z * s
    xx = x * xs
    xy = x * ys
    xz = x * zs
    xw = w * xs
    yy = y * ys
    yz = y * zs
    yw = w * ys
    zz = z * zs
    zw = w * zs

    return np.array([[1 - (yy + zz), (xy - zw), (xz + yw)], [(xy + zw),
        1 - (xx + zz), (yz - xw)], [(xz - yw), (yz + xw), 1 - (xx + yy)]])


def update(num, data, line):
    # print(data[:2, :num])
    # print(data[2, :num])
    print("-------------")
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

from matplotlib.animation import FuncAnimation 
def pygame_orientation():
    global orientation, line,xyzs

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-1.2, 1.2)
    ax.set_ylim3d(-1.2, 1.2)
    ax.set_zlim3d(-1.2, 1.2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    xyzs = []
    for row in orientation.Q[0:1500,:]:
        xyz = rotation_matrix(row) @ np.array([[0], [-1], [0]])
        xyzs.append((xyz[0,0], xyz[1, 0], xyz[2, 0]))
    xyzs = np.array(xyzs)

    # data = np.array(list(gen(1000))).T
    data = xyzs
    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

    # ax.plot(xyzs[:, 0], xyzs[:, 1], xyzs[:, 2], label="[0 0 1]^T transformed by q")
    ani = FuncAnimation(fig, update, 10000, fargs=(data, line), interval=2, blit=False)
    plt.show()

def plot_kalman():
    global uArray, buarray, xhatarr, altArr, ayArr, timeArr, stateArray, apogeeTime, temperature, csv
    print(np.max(xhatarr[:,0]))
    plt.subplot(311)
    plt.title("Position (m)")
    plt.plot(timeArr, altArr, label="Barometric Position")
    # plt.plot(timeArr, ayArr, label="Upwards acceleration",color='y')
    plt.plot(timeArr, xhatarr[:,0], label="Kalman Position")
    plt.legend()
    plt.axvline(x=apogeeTime, ls='--')

    plt.subplot(312)
    plt.title("Velocity (m/s)")
    # plt.scatter(timeArr[1:], np.diff(altArr)/np.diff(timeArr), label="Velocity (dBaro/dt)")
    # plt.plot(timeArr[1:], np.diff(xhatarr[:,0])/np.diff(timeArr), label="Numerical Diff Velocity")
    plt.plot(timeArr, xhatarr[:,1], label="Kalman Velocity")
    # plt.plot(timeArr, ayArr, label="Upwards acceleration")
    plt.legend()
    plt.axvline(x=apogeeTime, ls='--')

    plt.subplot(313)
    plt.title("Accel (m/s/s)")
    # plt.scatter(timeArr[1:], np.diff(altArr)/np.diff(timeArr), label="Velocity (dBaro/dt)")
    plt.plot(timeArr, ayArr, label="Raw acceleration")
    # plt.plot(timeArr, xhatarr[:,2], label="Kalman Accel")
    plt.legend()
    plt.axvline(x=apogeeTime, ls='--')

    gyro_data = None
    if "wx_raw" in csv:
        gyro_data = np.array([csv["wx_raw"] / 32.8,csv["wy_raw"] / 32.8, csv["wz_raw"] / 32.8]).T
    elif "wx" in csv:
        gyro_data = np.array([csv["wx"],csv["wy"], csv["wz"]]).T
    if gyro_data is not None:
        plt.subplot(224)
        # plt.title("Temperature (C) over time (s)")
        # plt.plot(timeArr, temperature, label="Temperature (C)")
        plt.title("Angular rate over time")
        plt.plot(timeArr, gyro_data[:,0], label="wx (deg/s)")
        plt.plot(timeArr, gyro_data[:,1], label="wy (deg/s)")
        plt.plot(timeArr, gyro_data[:,2], label="wz (deg/s)")
        plt.xlim(apogeeTime-35, apogeeTime + 1)
        plt.axvline(x=apogeeTime, ls='--')
        plt.legend()

    # plt.figure()
    # plt.plot(timeArr, altArr, label="Barometric Position")
    # plt.plot(timeArr, xhatarr[:,0], label="Kalman Position")
    # plt.plot(timeArr, xhatarr[:,1], label="Kalman Velocity")
    # plt.plot(timeArr, xhatarr[:,2], label="Kalman Accel")
    # plt.plot(timeArr, ayArr, label="Raw acceleration")
    # plt.plot(timeArr, stateArray, label="state")
    # plt.legend()

def plot_altitude():
    global uArray, buarray, xhatarr, altArr, ayArr, timeArr
    plt.plot(timeArr, altArr)

def plot_accel():
    plt.plot(timeArr, csv['ax'], label="ax")
    plt.plot(timeArr, csv['ay'], label="ay")
    plt.plot(timeArr, csv['az'], label="az")
    plt.legend()

def plot_mag():
    global csv, timeArr, altArr
    
    if False:
        plt.scatter(csv['imu1_mag_x'],csv['imu1_mag_y'])
        plt.scatter(csv['imu1_mag_y'],csv['imu1_mag_z'])
        plt.scatter(csv['imu1_mag_x'],csv['imu1_mag_z'])
        plt.xlim(-3000, 3000)
        plt.ylim(-3000, 3000)


    # on FCBV0, we negate x and y per https://learn.sparkfun.com/tutorials/lsm9ds1-breakout-hookup-guide/all
    mag_x = csv['imu1_mag_x'] * -1
    mag_y = csv['imu1_mag_y'] * -1
    mag_z = csv['imu1_mag_z']

    min_x = min(mag_x)
    max_x = max(mag_x)
    min_y = min(mag_y)
    max_y = max(mag_y)
    min_z = min(mag_z)
    max_z = max(mag_z)

    print("X range: ", min_x, max_x)
    print("Y range: ", min_y, max_y)
    print("Z range: ", min_z, max_z)

    mag_calibration = [ (max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]
    print("Final calibration in uTesla:", mag_calibration)

    cal_mag_x = [x - mag_calibration[0] for x in mag_x]
    cal_mag_y = [y - mag_calibration[1] for y in mag_y]
    cal_mag_z = [z - mag_calibration[2] for z in mag_z]

    if True:
        plt.figure()
        plt.scatter(cal_mag_x, cal_mag_y, color='r')
        plt.scatter(cal_mag_y, cal_mag_z, color='g')
        plt.scatter(cal_mag_z, cal_mag_x, color='b')
        plt.xlim(-3000, 3000)
        plt.ylim(-3000, 3000)

    return np.array([cal_mag_x, cal_mag_y, cal_mag_z]).T


    ax = plt.axes(projection='3d')
    maxUt = 2.5
    ax.set_xlim3d(-maxUt, maxUt)
    ax.set_ylim3d(-maxUt, maxUt)
    ax.set_zlim3d(-maxUt, maxUt)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    # csv = csv.loc[1800:4000,:]
    print(timeArr)
    ax.plot(csv['imu1_mag_x_real'],csv['imu1_mag_y_real'],csv['imu1_mag_z_real'])
    ax.plot(csv['imu2_mag_x_real'],csv['imu2_mag_y_real'],csv['imu2_mag_z_real'])
    plt.figure()
    plt.plot(timeArr,csv['imu2_gyro_x_real'])
    plt.plot(timeArr,csv['imu2_gyro_y_real'])
    plt.plot(timeArr,csv['imu2_gyro_z_real'])
    
    # plt.plot(csv["baro_pres_avg"])

def output_mag_vec(mag):
    global timeArr, csv
    timeArr = timeArr-timeArr[0] - 100
    # return np.array([cal_mag_x, cal_mag_y, cal_mag_z]).T

    plt.figure()
    plt.subplot(411)
    plt.plot(timeArr,mag[:,0], label="X, uT")
    plt.plot(timeArr,mag[:,1], label="Y, uT")
    plt.plot(timeArr,mag[:,2], label="Z, uT")
    plt.xlim(25,125)
    plt.legend()
    plt.subplot(412)
    plt.plot(timeArr, csv["pos_z"], label="Alt, m")
    plt.plot(timeArr, csv["vel_z"], label="Vel, m/s")
    plt.xlim(25,125)
    plt.legend()
    plt.subplot(413)
    plt.plot(timeArr, csv["imu1_gyro_x_real"], label="Wx, rad/s")
    plt.plot(timeArr, csv["imu1_gyro_y_real"], label="Wy, rad/s")
    plt.plot(timeArr, csv["imu1_gyro_z_real"], label="Wz, rad/s")
    plt.legend()
    plt.xlim(25,125)
    plt.subplot(414)
    plt.plot(timeArr, csv["imu1_accel_x_real"], label="Ax, m/s/s")
    plt.plot(timeArr, csv["imu1_accel_y_real"], label="Ay, m/s/s")
    plt.plot(timeArr, csv["imu1_accel_z_real"], label="Az, m/s/s")
    plt.xlim(25,125)
    plt.legend()
    np.savetxt("magvec.mat", mag)

    plt.figure()
    plt.title("dt, seconds")
    plt.plot(timeArr[1:], np.diff(timeArr))
    # plt.plot(1/np.diff(timeArr))
    df = csv
    # plt.subplot(212)
    # plt.title("state")
    # plt.scatter(timeArr, csv['state'])
    plt.axvline(timeArr[np.where(df['state'] == 12)[0][0]], ls="--")
    plt.axvline(timeArr[np.where(df['state'] == 7)[0][0]], ls="--")
    plt.axvline(timeArr[np.where(df['state'] == 8)[0][0]], ls="--")
    plt.axvline(timeArr[np.where(df['state'] == 10)[0][0]], ls="--")
    plt.axvline(timeArr[np.where(df['state'] == 11)[0][0]], ls="--")

if __name__ == "__main__":
    make_fcb(3)
    mag = plot_mag()
    # make_goose()
    # make_drone_goose()
    # make_line_cutter()

    output_mag_vec(mag)

    # do_kalman()
    do_gyro_integration(mag)
    # plot_kalman()
    # plot_gyro()
    # plt.figure()

    # pygame_orientation()
    
    plt.show()
