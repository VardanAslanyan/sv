from pytlv.TLV import *


class DE55:
    all_emv = {"5f2a": "Terminal Currency Code", "5f34": "PAN Sequence Number", "82": "Application Interchange Profile",
               "84": "Dedicated File", "8a": "Auth Response Code", "95": "TVR", "9a": "Transaction Date",
               "9b": "TSI", "9c": "Transaction Type", "9f02": "Amount Auth", "9f03": "Amount Other",
               "9f09": "Application Version Number", "9f10": "Issuer Application Data", "9f1a": "Terminal Country Code",
               "9f1e": "Serial Number", "9f26": "Application Cryptogram", "9f27": "Cryptogram Information Data",
               "9f33": "Terminal Capabilities", "9f34": "Cardholder Verification Method", "9f35": "Terminal Type",
               "9f36": "Application Transaction Counter", "9f37": "Unpredictable Number",
               "9f41": "Transaction Seq Number", "4f": "Application Identifier",
               "9f53": "Transaction Category Code", "91": "Issuer Authentication Data"}
    key_list = list((all_emv.keys()))

    def __init__(self, emv_data: str):
        self.emv_data = emv_data.replace(" ", "").replace("\n", "").lower()

    @classmethod
    def __get_tag(cls):
        tlv = TLV(DE55.key_list)
        return tlv

    def __eq__(self, other):
        if not isinstance(other, DE55):
            raise Exception("The second one is not DE_55 obj")
        if dict(self.__get_tag().parse(self.emv_data)).keys() == dict(other.__get_tag().parse(other.emv_data)).keys():
            return True
        else:
            return False

    def __repr__(self):
        tlv = self.__get_tag().parse(self.emv_data)
        for k, v in sorted(tlv.items()):
            length = len(k)
            if length == 2:
                length = 6
            print(DE55.all_emv.get(k), ">"*(35 - len(DE55.all_emv.get(k))), k, "-" * length, v)
        print('================================================================================')

    def __len__(self):
        return len(self.emv_data)//2

    @classmethod
    def __dict__(cls):
        return DE55.all_emv

    def diff(self, other):
        if self.__eq__(other):
            print("They are equal")
        else:
            first = set(self.__get_tag().parse(self.emv_data).keys())
            second = set(other.__get_tag().parse(other.emv_data).keys())
            print("In First diff", first - second)
            print("In Second diff", second - first)


















