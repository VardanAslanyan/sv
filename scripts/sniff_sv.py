import socket
import binascii
from retry import retry
from datetime import datetime

from .parse_message import SV


@retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None,
                 destination=None, destination_port=None,
                 scenario=None):
    listen_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_data.bind((host, port))
    listen_data.listen(10)
    conn, address = listen_data.accept()
    conn.settimeout(32)
    print(conn, address)
    d = None
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                listen_data.settimeout(32)
                print("\nRequest>>>", data)
                print(data.hex())
                print('Time', datetime.now().time())
            except Exception as error:
                print(error)
                break
            if not data:
                print("Good bye!")
                break
            try:
                data_hex = binascii.hexlify(data)
                SV(data_hex.decode("utf-8")).__repr__()

                d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                d.connect((destination, destination_port))
                # for auto-reversal not to send ArCa
                # print(data)
                # if b'040020' in data:
                #     print('-----------------------autoreversal-------------------')
                # elif b'0400r' in data:
                #     print('sending with second field')
                # else:
                #     d.sendall(data)
                #     to_client = d.recv(1024)

                d.sendall(data)
                to_client = d.recv(1024)

            except Exception as ex:
                print(ex)
                break
            try:
                print("\n\nResponse>>>", to_client)
                print("Time", datetime.now().time())
                to_client_hex = binascii.hexlify(to_client)
                SV(to_client_hex.decode("utf-8")).__repr__()
                if scenario == 'nothing_pass_to_pos':
                    if b'210r' in to_client:
                        print('\n-----------------Created automatic_reversal nothing_pass_to_pos--------------\n')
                    elif b'410r' in to_client:
                        print('drop auto_reversal')
                    else:
                        conn.sendall(to_client)
                elif scenario == 'pass_reversal_to_pos':
                    if b'210r' in to_client:
                        print('\n-----------------Created automatic_reversal pass_reversal_to_pos-------------\n')
                    else:
                        conn.sendall(to_client)
                elif scenario == 'card_answer_AAC':
                    conn.sendall(
                        b'01240210r0\x00\x00\x0e\x80\x82\x00169051345200223731000000000000045800063010502700004922063010502600101893490693490600021010878051\x00\x14\x91\x08\xd4\xa3@\xe0\x00\x80\x00\x00\x8a\x0200')
                else:
                    conn.sendall(to_client)
            except Exception as ex:
                print(ex)
                break
            print("The end!")
    if d:
        d.close()
    if listen_data:
        listen_data.close()
    print('It is the end!')
