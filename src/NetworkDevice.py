import ipaddress

class NetworkDevice:
    device_id: int
    hostname: str
    ip_address: ipaddress.IPv4Address
    vendor: str
    model: str
    firmware_version: str
    status: str

    def __init__(self, data: dict):
        for key, value in data.items():
            if not isinstance(value, str):
                raise ValueError(f"Invalid type for field '{key}': Expected string, got {type(value).__name__}")
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