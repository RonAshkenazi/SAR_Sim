"""Simple grid-based particle filter producing heatmap."""
import numpy as np
from dataclasses import dataclass
from core.environment import Environment
from channel.models import LogDistanceChannel


@dataclass
class GridPFConfig:
    grid_res: float


class GridParticleFilter:
    def __init__(self, env: Environment, channel: LogDistanceChannel, cfg: GridPFConfig):
        self.env = env
        self.channel = channel
        xs = np.arange(0, env.x + cfg.grid_res, cfg.grid_res)
        ys = np.arange(0, env.y + cfg.grid_res, cfg.grid_res)
        self.xx, self.yy = np.meshgrid(xs, ys)
        self.weights = np.ones_like(self.xx)

    def update(self, scanner_pos, rssi, tx_power_dbm):
        pred = np.vectorize(lambda x, y: self.channel.rssi((x, y, scanner_pos[2]), scanner_pos, tx_power_dbm))
        expected = pred(self.xx, self.yy)
        residual = rssi - expected
        self.weights *= np.exp(-0.5 * (residual / self.channel.awgn_sigma_db) ** 2)
        self.weights /= np.sum(self.weights)

    def estimate(self):
        x = np.sum(self.xx * self.weights)
        y = np.sum(self.yy * self.weights)
        return x, y
