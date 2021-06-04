import socket
import binascii
from parse_message import SV


def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None, destination=None, destination_port=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
            s.bind((host, port))
            s.listen(5)
            conn, address = s.accept()
            d.connect((destination, destination_port))
            with conn:
                print('Connected by', address)
                while True:
                    data = conn.recv(1024)
                    data_hex = binascii.hexlify(data)
                    if not data:
                        break
                    with open("request.txt", "wb") as request_data:
                        request_data.write(data_hex)
                    w = SV("request.txt")
                    w.__repr__()
                    d.sendall(data)
                    to_client = d.recv(1024)
                    to_client_hex = binascii.hexlify(to_client)
                    with open("response.txt", "wb") as response_data:
                        response_data.write(to_client_hex)
                    f = SV("response.txt")
                    f.__repr__()
                    conn.sendall(to_client)




