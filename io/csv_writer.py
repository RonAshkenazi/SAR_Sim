"""CSV writer for scan data."""
import csv
from typing import Iterable, Dict


def write_csv(path: str, rows: Iterable[Dict]):
    fieldnames = ["ts", "x", "y", "z", "rssi", "mac_hash", "proto", "scanner_id", "emitter_id"]
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
