"""Timebase utilities for simulation."""
from dataclasses import dataclass

@dataclass
class TimeConfig:
    dt: float
    steps: int

    def timeline(self):
        """Generate simulation timestamps."""
        t = 0.0
        for _ in range(self.steps):
            yield t
            t += self.dt
