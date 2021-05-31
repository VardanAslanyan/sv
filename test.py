from collections import namedtuple

class SV:

    Data = namedtuple("Data", ["field", "length"])
    field_3 = Data(3, 6) # Processing code
    field_4 = Data(4, 12*2) # Amount Trx
    field_7 = Data(7, 10*2) # Tate and Time
    field_11 = Data(11, 6*2) # Systems Trace Audit Number
    field_12 = Data(12, 12*2) # Time, Local Transaction
    field_22 = Data(22, 3*2) # Point of Service Data Code
    field_24 = Data(24, 3*2) # Function Code
    field_25 = Data(25, 2*2) # Point of Service Condition Code
    field_35 = Data(35, 37*2) # Track 2 Data
    field_41 = Data(41, 8*2) # Card Acceptor Terminal Identification
    field_42 = Data(42, 15*2) # Merchant Identification
    field_49 = Data(49, 3*2) # Currency Code, Transaction
    field_52 = Data(52, 8*2) # Personal Identification Data
    field_55 = Data(55, None) # EMV Data, Length: 2-byte BCD Data:b … 255
    all_fields = (field_3, field_4, field_7, field_11, field_12, field_22, field_24,
                  field_25, field_35, field_41, field_42, field_49, field_52, field_55)

    def __init__(self, data):
        with open(data, "r") as message:
            req_data = message.read().replace(" ", "").replace("\n", "")
            self.message = req_data

    def get_mti(self):
        mti_hex = self.message[:8]
        bytes_object = bytes.fromhex(mti_hex)
        mti = bytes_object.decode("ASCII")
        return mti, mti_hex

    def bitmap(self):
        bitmap_len = 16
        mti_len = len(self.get_mti()[1])
        bitmap_hex = self.message[mti_len: mti_len + bitmap_len]
        return bitmap_hex

    def bitmap_to_bin(self):
        dec = int(self.bitmap(), 16)
        data = str(bin(dec))[2:]
        return f'{"0"*(64 - len(data))}{data}'

    def find_fields(self):
        source = self.bitmap_to_bin()
        fields = []
        for i in enumerate(source, 1):
            if i[1] == "1":
                fields.append(i[0])
        return fields

    def parse_data(self):
        source = self.find_fields()
        d = {}
        data = self.message[24:]
        for i in source:
            for j in SV.all_fields:
                if i == j.field:
                    field = self.rec_data(data, j.field, j.length)
                    print(field)

    @classmethod
    def rec_data(cls, data, field, field_len=None):

        return field, data[:field_len], data[field_len:]



if __name__ == '__main__':
    w = SV("message")
    print(w.get_mti()[0])
    print(w.bitmap())
    # print(w.bitmap_to_bin())
    print(w.find_fields())
    print(w.parse_data())
