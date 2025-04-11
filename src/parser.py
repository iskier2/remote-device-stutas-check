from typing import List
import csv
import io
from src.NetworkDevice import NetworkDevice
import logging

def csv_to_network_devices(csv_file: str) -> List[NetworkDevice]:
    devices = []
    reader = csv.DictReader(io.StringIO(csv_file))
    for i, row in enumerate(reader):
        try:
            device = NetworkDevice(row)
            devices.append(device)
        except ValueError as e:
            logging.error(f"row {i}: {e}")
    return devices

def get_current_statuses(csv_file: str) -> dict:
    current_statuses = {}
    reader = csv.DictReader(io.StringIO(csv_file))
    for row in reader:
        device_id = int(row["device_id"])
        current_statuses[device_id] = row["status"]
    return current_statuses
