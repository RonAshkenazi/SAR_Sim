"""Convert RSSI to distance estimates."""
import math
from dataclasses import dataclass


@dataclass
class RSSIModel:
    pl0_db: float
    n: float
    d0_m: float
    min_d_m: float
    max_d_m: float

    def to_distance(self, tx_power_dbm: float, rssi_dbm: float) -> float:
        d = self.d0_m * 10 ** ((tx_power_dbm - self.pl0_db - rssi_dbm) / (10 * self.n))
        return max(self.min_d_m, min(self.max_d_m, d))
