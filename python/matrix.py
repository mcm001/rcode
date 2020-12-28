#!/usr/bin/env python3

import sys

if "--noninteractive" in sys.argv:
    import matplotlib as mpl

    mpl.use("svg")

import frccontrol as fct
import math
import matplotlib.pyplot as plt
import numpy as np


class Flywheel(fct.System):
    def __init__(self, dt, qvel, rvel):
        self.q_vel = qvel
        self.r_vel = rvel

        """Flywheel subsystem.

        Keyword arguments:
        dt -- time between model/controller updates
        """
        state_labels = [("Angular velocity", "rad/s")]
        u_labels = [("Voltage", "V")]
        self.set_plot_labels(state_labels, u_labels)

        fct.System.__init__(
            self,
            np.array([[-12.0]]),
            np.array([[12.0]]),
            dt,
            np.zeros((1, 1)),
            np.zeros((1, 1)),
        )

    def create_model(self, states, inputs):
        # Number of motors
        num_motors = 1.0
        # Flywheel moment of inertia in kg-m^2
        J = 0.00032
        # Gear ratio
        G = 12.0 / 18.0

        return fct.models.flywheel(fct.models.MOTOR_775PRO, num_motors, J, G)

    def design_controller_observer(self):
        q = [9.42]
        r = [12.0]
        self.design_lqr(q, r)
        # self.place_controller_poles([0.87])
        self.design_two_state_feedforward()

        q_vel = self.q_vel
        r_vel = self.r_vel
        self.design_kalman_filter([q_vel], [r_vel])
        # self.place_observer_poles([0.3])


def main():
    dt = 0.00505
    flywheel1 = Flywheel(dt, 10.0, 0.01)

    # Set up graphing
    l0 = 0.1
    l1 = l0 + 5.0
    l2 = l1 + 0.1
    t = np.arange(0, l2 + 5.0, dt)

    refs = []

    # Generate references for simulation
    for i in range(len(t)):
        r = np.array([[9000 / 60 * 2 * math.pi]])
        refs.append(r)

    x_rec = np.zeros((flywheel1.sysd.states, 0))
    ref_rec = np.zeros((flywheel1.sysd.states, 0))
    u_rec = np.zeros((flywheel1.sysd.inputs, 0))
    y_rec = np.zeros((flywheel1.sysd.outputs, 0))

    # Run simulation
    r = refs[0]
    for i in range(len(refs)):
        next_r = refs[i]

        flywheel1.y = flywheel1.x + np.random.normal(scale=100.0)
        flywheel1.update(next_r)

        # Log states for plotting
        x_rec = np.concatenate((x_rec, flywheel1.x_hat), axis=1)
        ref_rec = np.concatenate((ref_rec, flywheel1.r), axis=1)
        u_rec = np.concatenate((u_rec, flywheel1.u), axis=1)
        y_rec = np.concatenate((y_rec, flywheel1.y), axis=1)

    flywheel1.plot_time_responses(t, x_rec, ref_rec, u_rec)

    plt.show()

if __name__ == "__main__":
    main()
