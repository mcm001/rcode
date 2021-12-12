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
    global timeArr, altArr, dt, ayArr
    csv = pd.read_csv("D:\\Documents\\Angry Goose TCC 5-15-21.txt")
    timeArr = csv['time']
    timeArr = timeArr / 1000
    timeArr = timeArr

    # Convert to mpss sans earth gravity
    # ayArr = csv['ay']
    # ayArr = ayArr - 1
    # ayArr = ayArr * 9.81
    ayArr = csv['ay']**2+csv['ax']**2+csv['az']**2
    ayArr=np.sqrt(ayArr)
    ayArr = ayArr - 1
    ayArr = ayArr * 9.81

    # Already in meters
    altArr = csv['alt']

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

def make_fcb():
    global timeArr, altArr, dt, ayArr
    # df = pd.read_csv("D:\\Downloads\\output-post.csv")
    df = pd.read_csv("D:\\Downloads\\fcb-06-20-2021-output-post(1).csv")
    timeArr = df["timestamp_s"] / 1000
    # ayArr = df["imu_accel_y_avg"] - 9.81
    ayArr = df['imu_accel_x_avg']**2+df['imu_accel_y_avg']**2+df['imu_accel_z_avg']**2
    ayArr=np.sqrt(ayArr)
    ayArr = ayArr - 9.81
    altArr = (df["baro_temp_avg"] / -0.0065) * (1 - pow(df["baro_pres_avg"] / df["baro_pres_avg"][0], 287.0474909 * -0.0065 / 9.80665)) * 10
    dt = np.mean(np.diff(timeArr))

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

    # sysc = ct.ss(np.array([[0,1],[0,0]]), np.array([[0],[1]]), np.array([1,0]), np.array([0]))
    # sysd = sysc.sample(dt)  # Discretize model
    sysd = ct.ss(np.array([[1, dt, dt* dt /2],[0,1, dt],[0,0,1]]), np.array([[0,0],[0,0],[0,0]]), np.array([[1,0,0],[0,0,1]]), np.array([[0, 0], [0, 0]]))
    print(sysd)

    # Q is our process noise covariance
    # It's [pos variance, vel variance, accel variance]^t
    # R is measurement noise (how sure we are about out measurement)
    Q = make_cov_matrix([0.5, 6, 1])
    R = make_cov_matrix([8, 2])

    kalman_gain, P_steady = kalmd(sysd, Q, R)
    print(kalman_gain)

    # We assume we start at 0 position and velocity
    xhatarr = []
    x_hat = np.array([[0], [0], [0]])

    uArray = []
    buarray  = []
    last_alt = 0
    state = 0
    stateArray = []

    for (t, accel, altitude) in zip(timeArr, ayArr, altArr):
        if state >= 2:
            accel = 0

        # uArray.append(u[0,0])
        # bu = np.dot(sysd.B, u)
        # buarray.append([bu[0,0], bu[1,0]])
        u = np.array([[0],[0]])
        y = np.array([[altitude], [accel]])
        # y = np.array([[0], [0]])

        # predict
        x_hat = sysd.A @ x_hat + sysd.B @ u

        # correct
        x_hat += kalman_gain @ (
            y - sysd.C @ x_hat - sysd.D @ u
        )

        xhatarr.append([x_hat[0,0], x_hat[1,0], x_hat[2, 0]])

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

def plot_bu():
    global uArray, buarray, xhatarr, timeArr
    plt.plot(timeArr, uArray, label="Control input")
    plt.plot(timeArr, buarray[:,0], label="delta position")
    plt.plot(timeArr, buarray[:,1], label="Delta accel")
    plt.legend()

def plot_kalman():
    global uArray, buarray, xhatarr, altArr, ayArr, timeArr, stateArray, apogeeTime
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
    plt.plot(timeArr[1:], np.diff(xhatarr[:,0])/np.diff(timeArr), label="Numerical Diff Velocity")
    plt.plot(timeArr, xhatarr[:,1], label="Kalman Velocity")
    # plt.plot(timeArr, ayArr, label="Upwards acceleration")
    plt.legend()
    plt.axvline(x=apogeeTime, ls='--')

    plt.subplot(313)
    plt.title("Accel (m/s/s)")
    # plt.scatter(timeArr[1:], np.diff(altArr)/np.diff(timeArr), label="Velocity (dBaro/dt)")
    plt.plot(timeArr, ayArr, label="Raw acceleration")
    plt.plot(timeArr, xhatarr[:,2], label="Kalman Accel")
    plt.legend()
    plt.axvline(x=apogeeTime, ls='--')

    # plt.subplot(313)
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

if __name__ == "__main__":
    # make_fcb()
    make_goose()
    # make_drone_goose()
    # make_line_cutter()

    do_kalman()
    plot_kalman()
    # plt.figure()
    # plot_bu()
    plt.show()