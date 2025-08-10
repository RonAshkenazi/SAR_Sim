"""BLE advertisement simulator."""
import os
import hashlib


def random_mac():
    return ":".join(f"{b:02x}" for b in os.urandom(6))


def mac_hash(mac: str) -> str:
    return hashlib.sha1(mac.encode()).hexdigest()[:12]


def generate_advertisement(mac: str | None = None) -> dict:
    mac = mac or random_mac()
    return {"mac_hash": mac_hash(mac), "proto": "ble"}
