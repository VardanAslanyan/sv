import socket
import binascii
from .parse_message import SV
from retry import retry


@retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None, destination=None, destination_port=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(10)
        conn, address = s.accept()
        with conn:
            data = conn.recv(1024)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
                d.connect((destination, destination_port))
                data_hex = binascii.hexlify(data)
                try:
                    SV(data_hex.decode("utf-8")).__repr__()
                except Exception as ex:
                    print(ex)
                finally:
                    d.sendall(data)
                    to_client = d.recv(1024)
                    to_client_hex = binascii.hexlify(to_client)
                try:
                    SV(to_client_hex.decode("utf-8")).__repr__()
                except Exception as ex:
                    print(ex)
                finally:
                    conn.sendall(to_client)









