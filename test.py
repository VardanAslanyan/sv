
with open("message", "r") as message:
    req_200 = message.read().replace(" ", "").replace("\n", "")
    print(req_200)
    MTI_hex = req_200[:8]
    print(MTI_hex)
    bytes_object = bytes.fromhex(MTI_hex)
    MTI = bytes_object.decode("ASCII")
    print(MTI)


