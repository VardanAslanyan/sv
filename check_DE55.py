from tlv_parser import DE_55
# import iso8583
# from iso8583.specs import default_ascii as spec
# from iso8583.tools import pp
# import pprint

#
# s = b"02003230058020c08000000000000000002000050616313000001521050616311805920000335413330089020011=25126010793608052101087821000878051"
#
# doc_dec, doc_enc = iso8583.decode(s, spec)
# pprint.pprint(doc_dec)

field_55_android = """  

 5f 34 01 25 82 02 30 00 84 07 a0

00 00 00 04 30 60 95 05 00 00 04 80 00 9a 03 21

05 19 9b 02 e8 00 9c 01 00 9f 02 06 00 00 00 00

10 00 9f 03 06 00 00 00 00 00 00 9f 09 02 00 02

9f 10 12 02 10 a0 80 0f 24 00 00 00 00 00 00 00

00 00 00 00 ff 9f 1a 02 00 51 9f 1e 08 30 30 30

32 32 31 33 31 9f 26 08 7b 22 f1 00 dc d8 0a 5e

9f 27 01 80 9f 33 03 e0 f8 c8 9f 34 03 42 03 00

9f 35 01 22 9f 36 02 00 01 9f 37 04 73 f6 f0 7c

9f 41 04 00 00 00 02 4f 07 a0 00 00 00 04 30 60

9f 53 01 52        5f 2a 02 00 51                            
           
 """ #

ing_field_55 = """4F 07 A0 00 00 00 04 30 60 5F 2A 02 00 51 82 02 30 00 84 07
                A0 00 00 00 04 30 60 95 05 08 00 04 80 00 9A 03
                21 05 13 9B 02 E8 00 9C 01 00 9F 02 06 00 00 00
                00 10 00 9F 03 06 00 00 00 00 00 00 9F 09 02 00
                02 9F 10 12 02 10 A0 00 0F 24 00 00 00 00 00 00
                00 00 00 00 00 FF 9F 1A 02 00 51 9F 1E 08 30 34
                31 39 34 30 35 39 9F 26 08 7B 9F 6C BB DA BF 21
                1C 9F 27 01 80 9F 33 03 E0 F0 C8 9F 34 03 42 03
                00 9F 35 01 22 9F 36 02 00 03 9F 37 04 D1 E8 45
                1B 9F 41 03 00 00 46 9F 53 01 52 5F 34 01 25"""  #

if __name__ == '__main__':
    # pass
    test1 = DE_55(field_55_android)
    test1.__repr__()
    test2 = DE_55(ing_field_55)
    test2.__repr__()
    test1.diff(test2)
    # print(test1 == test2)
    # print(len(test1))
    # print(len(test2))
    # print(test1.__dict__())
