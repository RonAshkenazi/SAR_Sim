"""Motion models for scanner."""
import math
import random
from dataclasses import dataclass
from typing import List, Tuple
from core.environment import Environment


@dataclass
class MotionModel:
    env: Environment
    speed: float

    def step(self, pos: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
        raise NotImplementedError


@dataclass
class LawnMower(MotionModel):
    lane_spacing: float
    altitude: float

    def __post_init__(self):
        self.direction = 1
        self.x = 0.0
        self.y = 0.0

    def step(self, pos, t):
        dt = self.speed
        x, y, _ = pos
        x += self.direction * dt
        if x > self.env.x or x < 0:
            self.direction *= -1
            x = max(0, min(self.env.x, x))
            y += self.lane_spacing
        if y > self.env.y:
            y = 0
        return (x, y, self.altitude)


@dataclass
class RandomWalk(MotionModel):
    altitude: float

    def step(self, pos, t):
        angle = random.uniform(0, 2 * 3.14159)
        dx = self.speed * random.uniform(0.5, 1.5) * math.cos(angle)
        dy = self.speed * random.uniform(0.5, 1.5) * math.sin(angle)
        x = min(max(pos[0] + dx, 0), self.env.x)
        y = min(max(pos[1] + dy, 0), self.env.y)
        return (x, y, self.altitude)


@dataclass
class WaypointPath(MotionModel):
    waypoints: List[Tuple[float, float, float]]
    index: int = 0

    def step(self, pos, t):
        if not self.waypoints:
            return pos
        target = self.waypoints[self.index]
        x, y, z = pos
        tx, ty, tz = target
        dx, dy, dz = tx - x, ty - y, tz - z
        dist = (dx**2 + dy**2 + dz**2) ** 0.5
        if dist < self.speed:
            self.index = (self.index + 1) % len(self.waypoints)
            return target
        ratio = self.speed / dist
        return (x + dx * ratio, y + dy * ratio, z + dz * ratio)
