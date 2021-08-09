import socket
import binascii
from .parse_message import SV
from retry import retry


@retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None, destination=None, destination_port=None):
    listen_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_data.bind((host, port))
    listen_data.listen(10)
    conn, address = listen_data.accept()
    conn.settimeout(2)
    d = None
    with conn:
        while True:
            data = conn.recv(1024)
            listen_data.settimeout(5)  # TODO check work correct or not
            if not data:
                print("Good day my brother!")
                break
            try:
                data_hex = binascii.hexlify(data)
                SV(data_hex.decode("utf-8")).__repr__()
            except Exception as ex:
                print(ex)
            finally:
                d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                d.connect((destination, destination_port))
                d.sendall(data)
                to_client = d.recv(1024)
            try:
                to_client_hex = binascii.hexlify(to_client)
                SV(to_client_hex.decode("utf-8")).__repr__()
            except Exception as ex:
                print(ex)
            finally:
                # print(to_client)
                # x = to_client.replace(b'0002101', b'9142101')
                # conn.sendall(x)
                conn.sendall(to_client)
                print("The end!")
    d.close()
    listen_data.close()
    print('It is the end!')










