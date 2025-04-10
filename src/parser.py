import ipaddress
from dataclasses import dataclass
from typing import List
import csv
from src.logger import write_log
import io

class NetworkDevice:
    device_id: int
    hostname: str
    ip_address: ipaddress.IPv4Address
    vendor: str
    model: str
    firmware_version: str
    status: str

    def __init__(self, data: dict):
        if data["status"] not in {"online", "offline"}:
            raise ValueError(f"Invalid status: {data['status']}")

        try:
            self.device_id = int(data["device_id"])
        except ValueError:
            raise ValueError(f"Invalid device_id: {data['device_id']}")

        try:
            self.ip_address = ipaddress.ip_address(data["ip_address"])
        except ValueError:
            raise ValueError(f"Invalid IP address: {data['ip_address']}")

        self.hostname=data["hostname"]
        self.vendor=data["vendor"]
        self.model=data["model"]
        self.firmware_version=data["firmware_version"]
        self.status=data["status"]

def csv_to_network_devices(csv_file) -> List[NetworkDevice]:
    devices = []
    reader = csv.DictReader(io.StringIO(csv_file))
    for i, row in enumerate(reader):
        try:
            device = NetworkDevice(row)
            devices.append(device)
        except ValueError as e:
            write_log(i, row, e)
    return devices

def get_current_statuses(csv_file) -> dict:
    current_statuses = {}
    reader = csv.DictReader(io.StringIO(csv_file))
    for row in reader:
        device_id = int(row["device_id"])
        current_statuses[device_id] = row["status"]
    return current_statuses
