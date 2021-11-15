import socket
import binascii
from .parse_message import SV
from retry import retry


@retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
def sniffer_data(host=socket.gethostbyname(socket.gethostname()), port=None,
                 destination=None, destination_port=None,
                 scenario=None):
    listen_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_data.bind((host, port))
    listen_data.listen(10)
    conn, address = listen_data.accept()
    conn.settimeout(30)
    print(conn, address)
    d = None
    with conn:
        while True:
            data = conn.recv(1024)
            listen_data.settimeout(30)  # TODO check work correct or not
            print(data)
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
            # finally:

            try:
                to_client_hex = binascii.hexlify(to_client)
                SV(to_client_hex.decode("utf-8")).__repr__()

                print(to_client)
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
                else:
                    conn.sendall(to_client)
            except Exception as ex:
                print(ex)
                break
            # finally:


                # print(to_client)
                # if b'0210r' in to_client:
                #     x = to_client.replace(b'0003401', b'1163401')
                #     conn.sendall(x)
                # else:
                #     conn.sendall(to_client)

            print("The end!")
    d.close()
    listen_data.close()
    print('It is the end!')










