import numpy as np
from ahrs.common.orientation import q2R, ecompass, acc2q
from ahrs.common.mathfuncs import cosd, sind, skew

class EKF:
    def __init__(self,
        gyr: np.ndarray = None,
        acc: np.ndarray = None,
        mag: np.ndarray = None,
        frequency: float = 100.0,
        frame: str = 'NED',
        **kwargs):
        self.gyr = gyr
        self.acc = acc
        self.mag = mag
        self.frequency = frequency
        self.frame = frame                          # Local tangent plane coordinate frame
        self.Dt = kwargs.get('Dt', 1.0/self.frequency)
        self.q0 = kwargs.get('q0')
        self.P = np.identity(4)                     # Initial state covariance
        self.R = self._set_measurement_noise_covariance(**kwargs)
        self._set_reference_frames(kwargs.get('magnetic_ref'), self.frame)
        # Process of data is given
        # if self.gyr is not None and self.acc is not None:

        self.Q = self._compute_all(self.frame)

    def _set_measurement_noise_covariance(self, **kw) -> np.ndarray:
        self.noises = np.array(kw.get('noises', [0.3**2, 0.5**2, 0.8**2]))
        if 'var_gyr' in kw:
            self.noises[0] = kw.get('var_gyr')
        if 'var_acc' in kw:
            self.noises[1] = kw.get('var_acc')
        if 'var_mag' in kw:
            self.noises[2] = kw.get('var_mag')
        self.g_noise, self.a_noise, self.m_noise = self.noises
        return np.diag(np.repeat(self.noises[1:], 3))

    def _set_reference_frames(self, mref: float, frame: str = 'NED') -> None:
        if frame.upper() not in ['NED', 'ENU']:
            raise ValueError(f"Invalid frame '{frame}'. Try 'NED' or 'ENU'")
        # Magnetic Reference Vector
        if mref is None:
            # Local magnetic reference of Munich, Germany
            from ahrs.common.mathfuncs import MUNICH_LATITUDE, MUNICH_LONGITUDE, MUNICH_HEIGHT
            from ahrs.utils.wmm import WMM
            wmm = WMM(latitude=MUNICH_LATITUDE, longitude=MUNICH_LONGITUDE, height=MUNICH_HEIGHT)
            self.m_ref = np.array([wmm.X, wmm.Y, wmm.Z]) if frame.upper() == 'NED' else np.array([wmm.Y, wmm.X, -wmm.Z])
        elif isinstance(mref, (int, float)):
            cd, sd = cosd(mref), sind(mref)
            self.m_ref = np.array([cd, 0.0, sd]) if frame.upper() == 'NED' else np.array([0.0, cd, -sd])
        else:
            self.m_ref = np.copy(mref)
        self.m_ref /= np.linalg.norm(self.m_ref)
        # Gravitational Reference Vector
        self.a_ref = np.array([0.0, 0.0, -1.0]) if frame.upper() == 'NED' else np.array([0.0, 0.0, 1.0])

    def _compute_all(self, frame: str) -> np.ndarray:
        """
        Estimate the quaternions given all sensor data.

        Attributes ``gyr``, ``acc`` MUST contain data. Attribute ``mag`` is
        optional.

        Returns
        -------
        Q : numpy.ndarray
            M-by-4 Array with all estimated quaternions, where M is the number
            of samples.

        """
        # if self.acc.shape != self.gyr.shape:
        #     raise ValueError("acc and gyr are not the same size")
        num_samples = len(self.gyr)
        Q = np.zeros((num_samples, 4))
        Q[0] = self.q0
        if self.mag is not None:
            ###### Compute attitude with MARG architecture ######
            if self.q0 is None:
                Q[0] = ecompass(self.acc[0], self.mag[0], frame=frame, representation='quaternion')
            Q[0] /= np.linalg.norm(Q[0])
            # EKF Loop over all data
            for t in range(1, num_samples):
                if self.acc is None:
                    Q[t] = self.updateAll(q=Q[t-1], gyr=self.gyr[t], mag=self.mag[t], mode="mag")
                else:
                    Q[t] = self.updateAll(Q[t-1], self.gyr[t], self.acc[t], self.mag[t], mode="mag")
            return Q
        ###### Compute attitude with IMU architecture ######
        if self.q0 is None:
            Q[0] = acc2q(self.acc[0])
        Q[0] /= np.linalg.norm(Q[0])
        # EKF Loop over all data
        for t in range(1, num_samples):
            Q[t] = self.updateAll(Q[t-1], self.gyr[t], self.acc[t], mode="accel")
        return Q

    def Omega(self, x: np.ndarray) -> np.ndarray:
        """Omega operator.

        Given a vector :math:`\\mathbf{x}\\in\\mathbb{R}^3`, return a
        :math:`4\\times 4` matrix of the form:

        .. math::
            \\boldsymbol\\Omega(\\mathbf{x}) =
            \\begin{bmatrix}
            0 & -\\mathbf{x}^T \\\\ \\mathbf{x} & \\lfloor\\mathbf{x}\\rfloor_\\times
            \\end{bmatrix} =
            \\begin{bmatrix}
            0 & -x_1 & -x_2 & -x_3 \\\\
            x_1 & 0 & x_3 & -x_2 \\\\
            x_2 & -x_3 & 0 & x_1 \\\\
            x_3 & x_2 & -x_1 & 0
            \\end{bmatrix}

        This operator is constantly used at different steps of the EKF.

        Parameters
        ----------
        x : numpy.ndarray
            Three-dimensional vector.

        Returns
        -------
        Omega : numpy.ndarray
            Omega matrix.
        """
        return np.array([
            [0.0,  -x[0], -x[1], -x[2]],
            [x[0],   0.0,  x[2], -x[1]],
            [x[1], -x[2],   0.0,  x[0]],
            [x[2],  x[1], -x[0],   0.0]])

    def f(self, q: np.ndarray, omega: np.ndarray) -> np.ndarray:
        """Linearized function of Process Model (Prediction.)

        .. math::
            \\mathbf{f}(\\mathbf{q}_{t-1}) = \\Big(\\mathbf{I}_4 + \\frac{\\Delta t}{2}\\boldsymbol\\Omega_t\\Big)\\mathbf{q}_{t-1} =
            \\begin{bmatrix}
            q_w - \\frac{\\Delta t}{2} \\omega_x q_x - \\frac{\\Delta t}{2} \\omega_y q_y - \\frac{\\Delta t}{2} \\omega_z q_z\\\\
            q_x + \\frac{\\Delta t}{2} \\omega_x q_w - \\frac{\\Delta t}{2} \\omega_y q_z + \\frac{\\Delta t}{2} \\omega_z q_y\\\\
            q_y + \\frac{\\Delta t}{2} \\omega_x q_z + \\frac{\\Delta t}{2} \\omega_y q_w - \\frac{\\Delta t}{2} \\omega_z q_x\\\\
            q_z - \\frac{\\Delta t}{2} \\omega_x q_y + \\frac{\\Delta t}{2} \\omega_y q_x + \\frac{\\Delta t}{2} \\omega_z q_w
            \\end{bmatrix}

        Parameters
        ----------
        q : numpy.ndarray
            A-priori quaternion.
        omega : numpy.ndarray
            Angular velocity, in rad/s.

        Returns
        -------
        q : numpy.ndarray
            Linearized estimated quaternion in **Prediction** step.
        """
        Omega_t = self.Omega(omega)
        return (np.identity(4) + 0.5*self.Dt*Omega_t) @ q

    def dfdq(self, omega: np.ndarray) -> np.ndarray:
        """Jacobian of linearized predicted state.

        .. math::
            \\mathbf{F} = \\frac{\\partial\\mathbf{f}(\\mathbf{q}_{t-1})}{\\partial\\mathbf{q}} =
            \\begin{bmatrix}
            1 & - \\frac{\\Delta t}{2} \\omega_x & - \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_z\\\\
            \\frac{\\Delta t}{2} \\omega_x & 1 & \\frac{\\Delta t}{2} \\omega_z & - \\frac{\\Delta t}{2} \\omega_y\\\\
            \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_z & 1 & \\frac{\\Delta t}{2} \\omega_x\\\\
            \\frac{\\Delta t}{2} \\omega_z & \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_x & 1
            \\end{bmatrix}

        Parameters
        ----------
        omega : numpy.ndarray
            Angular velocity in rad/s.

        Returns
        -------
        F : numpy.ndarray
            Jacobian of state.
        """
        x = 0.5*self.Dt*omega
        return np.identity(4) + self.Omega(x)

    def h_both(self, q: np.ndarray) -> np.ndarray:
        C = q2R(q).T
        if len(self.z) < 4:
            return C @ self.a_ref
        return np.r_[C @ self.a_ref, C @ self.m_ref]

    def h_mag(self, q):
        C = q2R(q).T
        return C @ self.m_ref

    def dhdq_both(self, q: np.ndarray, mode: str = 'normal') -> np.ndarray:
        if mode.lower() not in ['normal', 'refactored']:
            raise ValueError(f"Mode '{mode}' is invalid. Try 'normal' or 'refactored'.")
        qw, qx, qy, qz = q

        v = np.r_[self.a_ref, self.m_ref]
        H = np.array([[-qy*v[2] + qz*v[1],  qy*v[1] + qz*v[2], -qw*v[2] + qx*v[1] - 2.0*qy*v[0],  qw*v[1] + qx*v[2] - 2.0*qz*v[0]],
                      [ qx*v[2] - qz*v[0],  qw*v[2] - 2.0*qx*v[1] + qy*v[0],  qx*v[0] + qz*v[2], -qw*v[0] + qy*v[2] - 2.0*qz*v[1]],
                      [-qx*v[1] + qy*v[0], -qw*v[1] - 2.0*qx*v[2] + qz*v[0],  qw*v[0] - 2.0*qy*v[2] + qz*v[1],  qx*v[0] + qy*v[1]]])
        if len(self.z) == 6:
            H_2 = np.array([[-qy*v[5] + qz*v[4],                qy*v[4] + qz*v[5], -qw*v[5] + qx*v[4] - 2.0*qy*v[3],  qw*v[4] + qx*v[5] - 2.0*qz*v[3]],
                            [ qx*v[5] - qz*v[3],  qw*v[5] - 2.0*qx*v[4] + qy*v[3],                qx*v[3] + qz*v[5], -qw*v[3] + qy*v[5] - 2.0*qz*v[4]],
                            [-qx*v[4] + qy*v[3], -qw*v[4] - 2.0*qx*v[5] + qz*v[3],  qw*v[3] - 2.0*qy*v[5] + qz*v[4],  qx*v[3] + qy*v[4]]])
            H = np.vstack((H, H_2))
        return 2.0*H

    def dhdq_mag(self, q: np.ndarray, mode: str = 'normal') -> np.ndarray:
        qw, qx, qy, qz = q
        v = self.m_ref
        H = np.array([[-qy*v[2] + qz*v[1],  qy*v[1] + qz*v[2], -qw*v[2] + qx*v[1] - 2.0*qy*v[0],  qw*v[1] + qx*v[2] - 2.0*qz*v[0]],
                      [ qx*v[2] - qz*v[0],  qw*v[2] - 2.0*qx*v[1] + qy*v[0],  qx*v[0] + qz*v[2], -qw*v[0] + qy*v[2] - 2.0*qz*v[1]],
                      [-qx*v[1] + qy*v[0], -qw*v[1] - 2.0*qx*v[2] + qz*v[0],  qw*v[0] - 2.0*qy*v[2] + qz*v[1],  qx*v[0] + qy*v[1]]])
        return 2.0*H

    def updateAll(self, q: np.ndarray, gyr: np.ndarray, acc: np.ndarray = None, mag: np.ndarray = None, mode: str = "both") -> np.ndarray:
        """
        Perform an update of the state.

        Parameters
        ----------
        q : numpy.ndarray
            A-priori orientation as quaternion.
        gyr : numpy.ndarray
            Sample of tri-axial Gyroscope in rad/s.
        acc : numpy.ndarray
            Sample of tri-axial Accelerometer in m/s^2.
        mag : numpy.ndarray
            Sample of tri-axial Magnetometer in uT.

        Returns
        -------
        q : numpy.ndarray
            Estimated a-posteriori orientation as quaternion.

        """
        if not np.isclose(np.linalg.norm(q), 1.0):
            raise ValueError("A-priori quaternion must have a norm equal to 1.")
        # Current Measurements
        g = np.copy(gyr)                # Gyroscope data as control vector
        a = np.copy(acc)

        if mode == "both":
            a_norm = np.linalg.norm(a)
            m_norm = np.linalg.norm(mag)
            self.z = np.r_[a/a_norm, mag/m_norm]
        elif mode == "mag":
            m_norm = np.linalg.norm(mag)
            self.z = np.r_[mag/m_norm]
        elif mode == "accel":
            a_norm = np.linalg.norm(a)
            self.z = np.r_[a/a_norm]
        else:
            raise ValueError()

        # Noises are (gyro, accel, mag)
        # If we have the mag, make a 6x6 with the diagonal of [accel, accel, accel, mag, mag, mag]
        # Otherwise just a 3x3 with [accel, accel, accel]
        self.R = np.diag(np.repeat(self.noises[1:] if mag is not None else self.noises[1], 3))
        if mode == "both":
            diagonal = np.repeat(self.noises[1:], 3)
        elif mode == "mag":
            diagonal = np.repeat(self.noises[2], 3)
        elif mode == "accel":
            diagonal = np.repeat(self.noises[1], 3)
        self.R = np.diag(diagonal)

        # ----- Prediction -----
        q_t = self.f(q, g)                  # Predicted State
        F   = self.dfdq(g)                  # Linearized Fundamental Matrix
        W   = 0.5*self.Dt * np.r_[[-q[1:]], q[0]*np.identity(3) + skew(q[1:])]  # Jacobian W = df/dω
        Q_t = 0.5*self.Dt * self.g_noise * W@W.T    # Process Noise Covariance
        P_t = F@self.P@F.T + Q_t            # Predicted Covariance Matrix
        # ----- Correction -----
        if mode == "mag":
            y = self.h_mag(q_t)
        else:
            y = self.h_both(q_t)                   # Expected Measurement function


        if mode == "mag":
            H = self.dhdq_mag(q_t)                # Linearized Measurement Matrix
        else:
            H = self.dhdq_both(q_t)                # Linearized Measurement Matrix

        v   = self.z - y                    # Innovation (Measurement Residual)
        S   = H@P_t@H.T + self.R            # Measurement Prediction Covariance
        K   = P_t@H.T@np.linalg.inv(S)      # Kalman Gain
        self.P = (np.identity(4) - K@H)@P_t
        self.q = q_t + K@v                  # Corrected state
        self.q /= np.linalg.norm(self.q)
        return self.q
