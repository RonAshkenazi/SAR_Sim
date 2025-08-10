"""Multilateration estimation."""
import numpy as np
from dataclasses import dataclass


@dataclass
class Multilateration:
    robust_loss: str = "huber"
    huber_delta: float = 1.0

    def estimate(self, positions, distances):
        """Estimate emitter position from scanner positions and distance estimates."""
        if len(positions) < 4:
            return None
        A = []
        b = []
        x0, y0, z0 = positions[0]
        d0 = distances[0]
        for (x, y, z), d in zip(positions[1:], distances[1:]):
            A.append([2*(x - x0), 2*(y - y0), 2*(z - z0)])
            b.append(d0**2 - d**2 - x0**2 + x**2 - y0**2 + y**2 - z0**2 + z**2)
        A = np.array(A)
        b = np.array(b)
        x_hat, *_ = np.linalg.lstsq(A, b, rcond=None)
        return x_hat
