import socket

HOST = '192.168.7.210'
PORT = 5050

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
        s.bind((HOST, PORT))
        s.listen(5)
        conn, address = s.accept()
        d.connect(("91.199.226.7", 10010))
        with conn:
            print('Connected by', address)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                d.sendall(data)
                to_client = d.recv(1024)
                print(to_client)
                conn.sendall(to_client)
