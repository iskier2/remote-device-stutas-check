from src.router import create_connection
from src.parser import csv_to_network_devices, get_current_statuses
from src.file_fetcher import read_remote_file
import argparse
import time

CSV_REMOTE_PATH = "/home/stauto/network_devices.csv"

def main(timeout):
    check_interval = 2
    sftp_client, close_connection = create_connection()
    end_time = time.time() + timeout
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
    close_connection()
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network devices monitor test')
    parser.add_argument('--timeout', type=int, required=True, help='Timeout in seconds for monitoring phase')
    timeout = parser.parse_args().timeout
    main(timeout)