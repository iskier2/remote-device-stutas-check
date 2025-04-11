from src.router import create_connection
from src.parser import csv_to_network_devices
from src.file_fetcher import read_remote_file
import argparse
import logging
from src.monitor import monitor
from src.consts import CSV_REMOTE_PATH, CHECK_INTERVAL
import sys
from src.consts import DisconectedDevice, DeviceNotFoundError

def main(repeats: int) -> int:
    logging.info(f"Start monitoring devices for {repeats} intervals of {CHECK_INTERVAL} seconds each.")
    try:
        sftp_client, close_connection = create_connection()
        file_content = read_remote_file(sftp_client, CSV_REMOTE_PATH)
        devices = csv_to_network_devices(file_content)
        online_devices = [dev for dev in devices if dev.status == 'online']
        if not online_devices:
            logging.error("No devices online.")
            raise DeviceNotFoundError
        monitor(online_devices, sftp_client, repeats)
        logging.info("Finished monitoring devices successfully.")
    except ConnectionError as e:
        raise ConnectionError
    except DisconectedDevice as e:
        raise DisconectedDevice
    except DeviceNotFoundError as e:
        raise DeviceNotFoundError
    except Exception as e:
        logging.error(f"An error occurred during monitoring: {e}")
        raise
    finally:
        if 'sftp_client' in locals():
            close_connection()
        logging.info("Closing the script.")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network devices monitor test')
    parser.add_argument('--timeout', type=int, required=True, help='Timeout in seconds for monitoring phase')
    parser.add_argument('--terminal_log', action='store_true', help='Enable terminal logging')
    repeats = parser.parse_args().timeout/CHECK_INTERVAL

    logging.basicConfig(
        filename='test_log.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if '--terminal_log' in sys.argv:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logging.getLogger().addHandler(console_handler)
    
    main(int(repeats))