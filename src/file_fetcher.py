def read_remote_file(sftp_client, filepath):
    try:
        with sftp_client.open(filepath, 'r') as remote_file:
            file_content = remote_file.read().decode('utf-8')
        print("Pomyślnie odczytano plik przy użyciu SFTP.")
        return file_content
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku przez SFTP:", e)
        return None
