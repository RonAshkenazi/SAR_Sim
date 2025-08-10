"""WiFi probe request packet simulator."""
import os
import hashlib


def random_mac():
    """Generate a random MAC address."""
    return ":".join(f"{b:02x}" for b in os.urandom(6))


def mac_hash(mac: str) -> str:
    """Return SHA1 hash of MAC address to anonymize."""
    return hashlib.sha1(mac.encode()).hexdigest()[:12]


def generate_probe(mac: str | None = None) -> dict:
    mac = mac or random_mac()
    return {"mac_hash": mac_hash(mac), "proto": "wifi"}
