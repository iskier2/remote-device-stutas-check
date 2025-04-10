import paramiko

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



