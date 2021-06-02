import socket

hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostbyname(hostname), 5050))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print(address)
    # t = s.recv(1024)
    # client_socket.recv(1024)
    client_socket.send(bytes("Welcome to server", "utf-8"))
    # client_socket.close()
    if address:
        d.connect(("109.75.38.80", 6090))
        msg = s.recv(1024)
        d.sendall(msg)
        print(msg.decode("utf-8"))

# print(socket.gethostbyname(hostname))
