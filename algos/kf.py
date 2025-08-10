"""Simple Kalman Filter for 3D constant velocity."""
import numpy as np
from dataclasses import dataclass


@dataclass
class KFConfig:
    dt: float
    q_pos: float
    q_vel: float
    r_pos: float


class KalmanFilter:
    def __init__(self, cfg: KFConfig):
        self.cfg = cfg
        dt = cfg.dt
        self.F = np.block([
            [np.eye(3), dt*np.eye(3)],
            [np.zeros((3,3)), np.eye(3)]
        ])
        q = cfg.q_pos
        r = cfg.q_vel
        self.Q = np.block([
            [q*np.eye(3), np.zeros((3,3))],
            [np.zeros((3,3)), r*np.eye(3)]
        ])
        self.H = np.block([np.eye(3), np.zeros((3,3))])
        self.R = cfg.r_pos * np.eye(3)
        self.x = np.zeros((6,1))
        self.P = np.eye(6)

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z: np.ndarray):
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ self.H) @ self.P
        return self.x[:3].flatten()
