import pytest
import time
import my_test

def monk_get_csv(status):
    headers = "device_id,hostname,ip_address,vendor,model,firmware_version,status"
    data = f"1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,{status}"
    return f"{headers}\n{data}"

def monk_connect():
    return None, lambda: None


def test_timeout_no_status_change(monkeypatch, capsys):
    def getOnlineCSV(sftp_client, filepath):
        return monk_get_csv("online")
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getOnlineCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    assert my_test.main(timeout=1) == 0

def test_offline_device_detection(monkeypatch):
    call_state = {"called": False}

    def getChangingCSV(sftp_client, filepath):
        status = "offline" if call_state["called"] else "online"
        call_state["called"] = True
        return monk_get_csv(status)
    
    monkeypatch.setattr(my_test, "create_connection", monk_connect)
    monkeypatch.setattr(my_test, "read_remote_file", getChangingCSV)
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    
    with pytest.raises(AssertionError):
        my_test.main(timeout=0.1)

