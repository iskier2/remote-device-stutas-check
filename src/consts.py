CSV_REMOTE_PATH = "/home/stauto/network_devices.csv"
CHECK_INTERVAL = 20
USERNAME = "stauto"
SSH_SERVER_PORT = 22

class DisconectedDevice(Exception):
    pass

class DeviceNotFoundError(Exception):
    pass

