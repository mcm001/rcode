#!/usr/bin/env python3

import frccontrol as fct
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

## Number of motors
#num_motors = 2.0
## Elevator carriage mass in kg
#m = 6.803886
## Radius of pulley in meters
#r = 0.0254
## Gear ratio
#G = 10.0

# Number of motors
num_motors = 2.0
# Elevator carriage mass in kg
m = 6.803886
# Radius of pulley in meters
r = 0.02762679089
# Gear ratio
G = 42.0 / 12.0 * 40.0 / 14.0

sysc = fct.models.elevator(fct.models.MOTOR_CIM, num_motors, m, r, G)
sysd = sysc.sample(0.020)
    
# generate a quiver plot from this
plt.figure()

xHat1 = []
xHat2 = []
xDot1 = []
xDot2 = []


q = [0.02, 0.4]
r = [12.0]
Q = np.diag(1.0 / np.square(q))
R = np.diag(1.0 / np.square(r))
# K = fct.lqr(sysc, Q, R) * 2
r = np.array([[5.0], [0.0]])

K = np.diag([5, 5.0])
print(K)

for x1 in np.arange(-math.pi, math.pi, math.pi / 8):
    for x2 in np.arange(-5.0, 5.0, math.pi / 8):
        # self.x_hat = self.sysd.A @ self.x_hat + self.sysd.B @ self.u
        x_hat = np.array([[x1], [x2]])
        # print(sysc.A)
        #x_dot = sysc.A @ x_hat + sysc.B @ K @ (r - x_hat) #+ sysd.B @ np.array[[0.0], [0.0]]\

        error = np.array([[math.pi / 2.0], [0]]) - x_hat
        feedback = K @ error
        
        # print(feedback)
        x_dot = (np.array([[x_hat[1, 0]], [-9.806 / 2.0 * math.sin(x_hat[0, 0])]])) #+ np.array([[0], [4.903]])) + feedback
        
        
        # print("xdot at %s, %s is (%s, %s)" % (x1, x2, x_dot[0, 0], x_dot[1, 0]))
        xHat1.append(x_hat[0, 0])
        xHat2.append(x_hat[1, 0])
        
        xDot1.append(x_dot[0, 0])
        xDot2.append(x_dot[1, 0])

x_hat = np.array([[math.pi / 2.0], [0]])
print("xdot is %s" % np.array([[x_hat[1, 0]], [-9.806 / 2.0 * math.sin(x_hat[0, 0])]]))

q = plt.quiver(xHat1, xHat2, xDot1, xDot2, angles="xy")
# plt.rc('text', usetex=True)
plt.scatter(math.pi / 2.0, 0, s=50)
plt.title("Closed loop pendulum phase plot with reference at $(\\frac{\\pi}{2}, 0)$")
plt.xlabel("Angle ($\\theta$)")
plt.ylabel("Angular velocity ($\\omega$)")
plt.show()
