import socket
import binascii
from .parse_message import SV
from retry import retry
from datetime import datetime, timedelta


@retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None, destination=None, destination_port=None,
                 now=None):
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    conn, address = s.accept()
    d = None
    while conn:
        data = conn.recv(1024)
        if not data:
            print("Good day!")
            break
        # print(str(datetime.now() + timedelta(seconds=5)))
        # if now == datetime.now() + timedelta(seconds=5):
        #     print("Time out!")
        #     break
        print()
        print(data)
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.connect((destination, destination_port))
        data_hex = binascii.hexlify(data)
        try:
            SV(data_hex.decode("utf-8")).__repr__()
        except Exception as ex:
            print(ex)
        finally:
            d.sendall(data)
            to_client = d.recv(1024)
            print()
            print(to_client)
            to_client_hex = binascii.hexlify(to_client)
        try:
            SV(to_client_hex.decode("utf-8")).__repr__()
        except Exception as ex:
            print(ex)
        finally:
            conn.sendall(to_client)
            print("The end!")
    d.close()
    s.close()










