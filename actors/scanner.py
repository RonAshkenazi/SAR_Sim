"""Scanner (drone) entity."""
from dataclasses import dataclass
from typing import List
from core.entity import Entity
from channel.models import LogDistanceChannel
from actors.motion import MotionModel


@dataclass
class Scanner(Entity):
    motion: MotionModel
    channel: LogDistanceChannel
    sample_rate_hz: float

    def step(self, t: float, emitters: List["Emitter"]):
        self.position = self.motion.step(self.position, t)
        for e in emitters:
            rssi = self.channel.rssi(e.position, self.position, e.tx_dbm)
            self.log(t, rssi=rssi, mac_hash=e.mac_hash, proto=e.proto, scanner_id=self.id, emitter_id=e.id)
