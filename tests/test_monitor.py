import pytest
import time
import my_test
from paramiko import SFTPClient
import src.monitor
from src.consts import DisconectedDevice, DeviceNotFoundError

def monk_get_csv(status: str, rows_number: int = 1) -> str:
    data = "device_id,hostname,ip_address,vendor,model,firmware_version,status"
    for i in range(rows_number):
        data += f"\n{i},hostname_{i},192.168.1.{i},vendor_{i},model_{i},firmware_{i},{status}"
    return data

def monk_connect() -> tuple:
    return None, lambda: None

def test_timeout_no_status_change(monkeypatch: pytest.MonkeyPatch) -> None:
    def getOnlineCSV(sftp_client: SFTPClient, filepath: str) -> str:
        return monk_get_csv("online")
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getOnlineCSV)
    monkeypatch.setattr(src.monitor, "read_remote_file", getOnlineCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    my_test.main(repeats=100) == 0

def test_offline_device_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    call_state = {"called": False}

    def getChangingCSV(sftp_client: SFTPClient, filepath: str) -> str:
        status = "offline" if call_state["called"] else "online"
        call_state["called"] = True
        return monk_get_csv(status)
    
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getChangingCSV)
    monkeypatch.setattr(src.monitor, "read_remote_file", getChangingCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    
    with pytest.raises(DisconectedDevice):
        my_test.main(repeats=100)

def test_reduce_row_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    call_state = {"called": False}

    def getChangingCSV(sftp_client: SFTPClient, filepath: str) -> str:
        rows_number = 1 if call_state["called"] else 2
        call_state["called"] = True
        return monk_get_csv("online", rows_number)
    
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getChangingCSV)
    monkeypatch.setattr(src.monitor, "read_remote_file", getChangingCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    
    with pytest.raises(DeviceNotFoundError):
        my_test.main(repeats=100)

def test_no_devices_online(monkeypatch: pytest.MonkeyPatch) -> None:
    def getEmptyCSV(sftp_client: SFTPClient, filepath: str) -> str:
        return monk_get_csv("offline", rows_number=0)
            
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getEmptyCSV)
    monkeypatch.setattr(src.monitor, "read_remote_file", getEmptyCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
            
    with pytest.raises(DeviceNotFoundError):
        my_test.main(repeats=100)

