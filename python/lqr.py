import control as ct
import frccontrol as fcnt
import numpy as np
import scipy as sp

fcnt.System

# def __make_cost_matrix(elems):
#     """Creates a cost matrix from the given vector for use with LQR.
#
#     The cost matrix is constructed using Bryson's rule. The inverse square
#     of each element in the input is taken and placed on the cost matrix
#     diagonal.
#
#     Keyword arguments:
#     elems -- a vector. For a Q matrix, its elements are the maximum allowed
#              excursions of the states from the reference. For an R matrix,
#              its elements are the maximum allowed excursions of the control
#              inputs from no actuation.
#
#     Returns:
#     State excursion or control effort cost matrix
#     """
#     return np.diag(1.0 / np.square(elems))
#
#
# kv = 2.9
# ka = 0.3
#
# # \mathbf{\dot{x}} &= [\frac{-kV}{kA}] \cdot v + \frac{1}{kA} \cdot V
# Q = np.array([1.0 / ((0.1 * 1) ** 2)])
# R = np.array([1.0 / (1.25 ** 2)])
#
# sysc = ct.StateSpace(
#     np.array([-kv / ka]),
#     np.array([1.0 / ka]),
#     np.array([1.0]),
#     np.array([0.0])
# )
# sysd = sysc.sample(0.02)
#
# N = np.zeros((sysd.A.shape[0], sysd.B.shape[1]))
# P = sp.linalg.solve_discrete_are(a=sysd.A, b=sysd.B, q=Q, r=R, s=N)
# K = np.linalg.solve(R + sysd.B.T @ P @ sysd.B, sysd.B.T @ P @ sysd.A + N.T)
#
# print(K)
