"""Environment definition for simulation space."""
from dataclasses import dataclass

@dataclass
class Environment:
    """3D environment boundaries in meters."""
    x: float
    y: float
    z: float

    def contains(self, position):
        """Check if a position tuple (x,y,z) is inside environment."""
        x, y, z = position
        return 0 <= x <= self.x and 0 <= y <= self.y and 0 <= z <= self.z
