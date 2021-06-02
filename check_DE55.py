from parse_message import SV

if __name__ == '__main__':
    w = SV("request.txt")
    w.__repr__()
    f = SV("response.txt")
    f.__repr__()

