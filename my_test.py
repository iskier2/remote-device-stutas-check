from src.ssh_tunel import connect_server, open_channel
from src.parser import csv_to_network_devices, get_current_statuses
from src.file_fetcher import read_remote_file
import argparse
import time
from dotenv import load_dotenv
import os
import paramiko
from io import StringIO

parser = argparse.ArgumentParser(description='Network devices monitor test')
parser.add_argument('--timeout', type=int, required=True, help='Timeout in seconds for monitoring phase')
timeout = parser.parse_args().timeout
check_interval = 2

load_dotenv()

SERVER_A_ADDRESS = os.environ["SERVER_A_ADDRESS"]
SERVER_B_ADDRESS = os.environ["SERVER_B_ADDRESS"]
SERVER_A_KEY = paramiko.RSAKey.from_private_key(StringIO(os.environ["SERVER_A_KEY"]))
SERVER_B_KEY = paramiko.RSAKey.from_private_key(StringIO(os.environ["SERVER_B_KEY"]))
CSV_REMOTE_PATH = "/home/stauto/network_devices.csv"
CSV_LOCAL_PATH = "network_devices.csv"
USERNAME = "stauto"

def test_devices():
    end_time = time.time() + timeout
    client_A = connect_server(SERVER_A_ADDRESS, 22, USERNAME, SERVER_A_KEY)
    channel = open_channel(client_A, SERVER_B_ADDRESS, 22)
    client_B = connect_server(SERVER_B_ADDRESS, 22, USERNAME, SERVER_B_KEY, sock=channel)
    sftp_client = client_B.open_sftp()
    file_content = read_remote_file(sftp_client, CSV_REMOTE_PATH)
    devices = csv_to_network_devices(file_content)
    online_devices = [dev for dev in devices if dev.status == 'online']

    time.sleep(check_interval)

    while time.time() < end_time:
        file_content = read_remote_file(sftp_client, CSV_REMOTE_PATH)
        current_statuses = get_current_statuses(file_content)
        print("check")
        for dev in online_devices:
            status = current_statuses[dev.device_id]
            assert status == 'online'

        time.sleep(check_interval)

    sftp_client.close()
    client_B.close()
    client_A.close()
test_devices()