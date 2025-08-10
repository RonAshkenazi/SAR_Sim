"""Radio channel models."""
import math
import random
from dataclasses import dataclass
from typing import Tuple


@dataclass
class LogDistanceChannel:
    pl0_db: float
    n: float
    shadow_sigma_db: float
    awgn_sigma_db: float
    d0_m: float = 1.0

    def path_loss(self, d: float) -> float:
        if d < self.d0_m:
            d = self.d0_m
        return self.pl0_db + 10 * self.n * math.log10(d / self.d0_m)

    def rssi(self, tx_pos: Tuple[float, float, float], rx_pos: Tuple[float, float, float], tx_power_dbm: float) -> float:
        dx = tx_pos[0] - rx_pos[0]
        dy = tx_pos[1] - rx_pos[1]
        dz = tx_pos[2] - rx_pos[2]
        d = math.sqrt(dx * dx + dy * dy + dz * dz)
        pl = self.path_loss(d)
        shadow = random.gauss(0, self.shadow_sigma_db)
        noise = random.gauss(0, self.awgn_sigma_db)
        return tx_power_dbm - pl + shadow + noise
