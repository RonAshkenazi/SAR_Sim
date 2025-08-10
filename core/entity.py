"""Base entity classes."""
from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class Entity:
    id: str
    position: Tuple[float, float, float]
    proto: str | None = None
    history: list = field(default_factory=list)

    def log(self, t, **data):
        entry = {"t": t, "x": self.position[0], "y": self.position[1], "z": self.position[2]}
        entry.update(data)
        self.history.append(entry)
