import paramiko
import os
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

SERVER_A_ADDRESS = os.environ["SERVER_A_ADDRESS"]
SERVER_B_ADDRESS = os.environ["SERVER_B_ADDRESS"]
SERVER_A_KEY = os.environ["SERVER_A_KEY"]
SERVER_B_KEY = os.environ["SERVER_B_KEY"]
CSV_REMOTE_PATH = "/home/stauto/network_devices.csv"
USERNAME = "stauto"

def connect_server(host, port, username, key, sock=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, pkey=key, sock=sock)
    return client

def open_channel(client_A, server_b_host, server_b_port):
    transport = client_A.get_transport()
    src_addr = ('127.0.0.1', 0)
    dest_addr = (server_b_host, server_b_port)
    channel = transport.open_channel("direct-tcpip", dest_addr, src_addr)
    print(f"Utworzono kanał do serwera B: {server_b_host}:{server_b_port}")
    return channel

def create_connection():
    try:
        a_key = paramiko.RSAKey.from_private_key(StringIO(SERVER_A_KEY))
        b_key = paramiko.RSAKey.from_private_key(StringIO(SERVER_B_KEY))
        client_A = connect_server(SERVER_A_ADDRESS, 22, USERNAME, a_key)
        channel = open_channel(client_A, SERVER_B_ADDRESS, 22)
        client_B = connect_server(SERVER_B_ADDRESS, 22, USERNAME, b_key, sock=channel)
        sftp_client = client_B.open_sftp()
        def close_connection():
            sftp_client.close()
            client_B.close()
            client_A.close()
        return sftp_client, close_connection
    except Exception as e:
        print(f"Error connecting to servers: {e}")
        raise

