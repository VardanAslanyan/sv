import socket
import binascii
from parse_message import SV


def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None, destination=None, destination_port=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
            s.bind((host, port))
            s.listen(10)
            conn, address = s.accept()
            d.connect((destination, destination_port))
            with conn:
                # while True:
                data = conn.recv(1024)
                data_hex = binascii.hexlify(data)
                # if not data:
                #     break
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







