from scripts import sniffer_data


if __name__ == '__main__':
    dest_address = "91.199.226.7"
    dest_port = 10010    
    while True:
        scenario = None
        #scenario = 'nothing_pass_to_pos'
        #scenario = 'pass_reversal_to_pos'
        
        sniffer_data(port=10050, destination=dest_address,
                     destination_port=dest_port, host="0.0.0.0",
                     scenario=scenario)

