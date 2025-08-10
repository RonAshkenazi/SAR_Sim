"""Emitter representing a device transmitting signals."""
from dataclasses import dataclass
from typing import Tuple
import protocols.wifi as wifi
import protocols.ble as ble


@dataclass
class Emitter:
    id: str
    proto: str
    tx_dbm: float
    position: Tuple[float, float, float]
    mac_hash: str

    @classmethod
    def create(cls, id: str, proto: str, tx_dbm: float, position: Tuple[float, float, float]):
        if proto == "wifi":
            pkt = wifi.generate_probe()
        else:
            pkt = ble.generate_advertisement()
        return cls(id=id, proto=proto, tx_dbm=tx_dbm, position=position, mac_hash=pkt["mac_hash"])

    def emit(self):
        return {"mac_hash": self.mac_hash, "proto": self.proto, "tx_dbm": self.tx_dbm}
