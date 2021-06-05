from collections import namedtuple
from tlv_parser import DE55


class SV:

    Data = namedtuple("Data", ["field", "length", "name"])
    mti = Data(0, 4*2, "Message Type ID")
    field_1 = Data(1, 8*2, "Secondary Bit-Map")
    field_2 = Data(2, None, "Primary Account Number")
    field_3 = Data(3, 6*2, "Processing code")
    field_4 = Data(4, 12*2, "Amount Trx")
    field_7 = Data(7, 10*2, "Tate and Time")
    field_11 = Data(11, 6*2, "Systems Trace Audit Number")
    field_12 = Data(12, 12*2, "Time, Local Transaction")
    field_14 = Data(14, 6*2, "Date, Expiration")
    field_15 = Data(15, 6*2, "Date, Settlement")
    field_22 = Data(22, 3*2, "Point of Service Data Code")
    field_24 = Data(24, 3*2, "Function Code")
    field_25 = Data(25, 2*2, "Point of Service Condition Code")
    field_30 = Data(30, None, "Amount, Original") #TODO check settlement
    field_35 = Data(35, None, "Track 2 Data")
    field_37 = Data(37, 12*2, "Retrieval Reference Number")
    field_38 = Data(38, 6*2, "Approval Code")
    field_39 = Data(39, 3*2, "Response Code")
    field_41 = Data(41, 8*2, "Card Acceptor Terminal Identification")
    field_42 = Data(42, 15*2, "Merchant Identification")
    field_44 = Data(44, None, "Additional Response Data") #TODO check this if possible
    field_45 = Data(45, None, "Track 1 Data")
    field_46 = Data(46, None, "Amount, fees")
    field_48 = Data(48, None, "Additional Data - Private")
    field_49 = Data(49, 3*2, "Currency Code, Transaction")
    field_52 = Data(52, 8*2, "Personal Identification Data")
    field_53 = Data(53, None, "COMMUNICATION KEY")
    field_54 = Data(54, None, "Amounts, Additional") #TODO check this if possible
    field_55 = Data(55, None, "EMV Data")
    field_62 = Data(62, None, "Customer Defined Response") #TODO check this if possible
    field_63 = Data(63, None, "Client Debts Data") #TODO check this if possible
    field_64 = Data(64, 8*2, "PRIMARY MAC DATA")
    all_fields = (field_2, field_3, field_4, field_7, field_11, field_12, field_22, field_24, field_25, field_30,
                  field_35, field_37, field_38, field_39, field_41, field_42, field_45,  field_46, field_48, field_49,
                  field_52, field_53, field_55, field_64)

    def __init__(self, data):
        with open(data, "r") as message:
            req_data = message.read().replace(" ", "").replace("\n", "")
            self.message = req_data[8:]

    def get_mti(self):
        mti_hex = self.message[:SV.mti.length]
        mti = self.hex_ascii(mti_hex)
        return mti

    def bitmap(self):
        self.get_mti()
        bitmap_hex = self.message[SV.mti.length: SV.mti.length + SV.field_1.length]
        return bitmap_hex

    def bitmap_to_bin(self):
        dec = int(self.bitmap(), 16)
        data = str(bin(dec))[2:]
        return f'{"0"*(64 - len(data))}{data}'

    def find_fields(self):
        source = self.bitmap_to_bin()
        fields = [i[0] for i in enumerate(source, 1) if i[1] == "1"]
        # for i in enumerate(source, 1):
        #     if i[1] == "1":
        #         fields.append(i[0])
        return fields

    def parse_data(self):
        source = self.find_fields()
        data_out = {}
        data = self.message[SV.mti.length + SV.field_1.length:]
        for i in source:
            for j in SV.all_fields:
                if i == j.field:
                    if i in (2, 35, 45, 46, 53):
                        length = 4
                        if i == 46:
                            length = 6
                        field_length_hex = data[:length]
                        field_length = int(self.hex_ascii(field_length_hex)) * 2
                        data = data[length:]
                        if i == 53:
                            data_out[i] = data[: field_length]
                        else:
                            data_out[i] = self.hex_ascii(data[: field_length])
                        data = data[field_length:]
                    elif i == 52 or i == 64:
                        data_out[i] = data[:j.length]
                        data = data[j.length:]
                    elif i == 55:
                        field_55_length = int(data[:4]) * 2
                        data = data[4:]
                        data_out[i] = DE55(str(data[:field_55_length]))
                    else:
                        data_out[i] = self.hex_ascii(data[:j.length])
                        data = data[j.length:]
        return data_out

    @classmethod
    def hex_ascii(cls, hex_data):
        bytes_object = bytes.fromhex(hex_data)
        data = bytes_object.decode("ASCII")
        return data

    @classmethod
    def print_24(cls, message_name):
        symbols = '-'*((38 - len(message_name))//2)
        return f"{symbols}{message_name}{symbols}"

    @classmethod
    def field_24_parse(cls, value: str):
        function_code = {'811': 'Network Key Change', '831': 'Echo Test', '400': 'Reversal'}
        if value in function_code.keys():
            SV.print_24(function_code.get(value))
        # if value == "811":
        #     return SV.print_24('Network Key Change')
        # elif value == "831":
        #     return SV.print_24('Echo Test')
        # elif value == "400":
        #     return SV.print_24('Reversal')
        else:
            return "-"*38

    def __repr__(self):
        print(f"\n{'-'*80}")
        data = self.parse_data()
        print(self.field_24_parse(data.get(24)))
        print("MTI>>", self.get_mti(), sep="")
        print("BITMAP>>", self.find_fields(), sep="")
        for k, v in data.items():
            for i in SV.all_fields:
                if k == i.field:
                    if k == 55:
                        print("\n-----Start EMV Data-----")
                        v.__repr__()
                    else:
                        if len(str(k)) == 1:
                            space = 1
                        else:
                            space = 0
                        print(f'{i.name}{">"*(40 - len(i.name) + space)}{k}{"-"*8}{v}')



