import time
import logging
from src.file_fetcher import read_remote_file
from src.parser import get_current_statuses
from src.consts import CSV_REMOTE_PATH, CHECK_INTERVAL
from src.consts import DisconectedDevice, DeviceNotFoundError

def monitor(online_devices, sftp_client, repeats):
    try:
        for _ in range(repeats):
            file_content = read_remote_file(sftp_client, CSV_REMOTE_PATH)
            current_statuses = get_current_statuses(file_content)

            for dev in online_devices:
                status = current_statuses[dev.device_id]
                assert status == 'online'

            logging.info(f"{len(online_devices)} devices online")

            time.sleep(CHECK_INTERVAL)
    except KeyError as e:
        logging.error(f"KeyError: Missing device ID in current statuses - {e}")
        raise DeviceNotFoundError
        
    except AssertionError as e:
        logging.error("Device status mismatch detected.")
        raise DisconectedDevice
