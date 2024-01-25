import sys

def intToBinary(x):
    return bin(x)[2:]

def rsa(x, e, n):
    y = 1;
    eBin = intToBinary(e)
    eLen = len(eBin)
    for i in range(len(eBin)):
        if (eBin[eLen-1-i] == '1'):
            y = (y * x) % n
        x = (x * x) % n
    return y

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 rsa.py <input_file> <key_file> <output_file>")
        sys.exit(1)

    key, e, n, message = "", 0, 0, ""
    input_file = sys.argv[1]
    key_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(key_file, "r") as f:
        key = f.read().splitlines()
        e = int(key[0])
        n = int(key[1])

    with open(input_file, "r") as f:
        message = f.read().splitlines()
        message = int(message[0])

    encrypted = rsa(message, e, n)

    with open(output_file, "w") as f:
        f.write(str(encrypted))