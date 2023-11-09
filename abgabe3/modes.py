import sys

def _padAndByte(plaintext, blocklength):
    plaintext = _string_to_binary(plaintext)
    if len(plaintext) % blocklength != 0:
        toAddZeros = blocklength - len(plaintext) % blocklength
        plaintext += '0' * toAddZeros
    return plaintext


def _binary_to_string(b):
    return ''.join(chr(int(''.join(str(x) for x in y), 2)) for y in zip(*[iter(b)]*8))

def _string_to_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a.encode(), b.encode())])

def blackbox_encrypt(byteString):
    return xor(byteString, _string_to_binary(key))

def blackbox_decrypt(byteString):
    return xor(byteString, _string_to_binary(key))

class modeECB():
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        return _binary_to_string(blackbox_encrypt(plaintext))

    def decrypt(self, ciphertext):
        ciphertext = _string_to_binary(ciphertext)
        return _binary_to_string(blackbox_decrypt(ciphertext))

class modeCBC():
    def __init__(self, iv):
        self.iv = iv
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        prev_ciphertext = self.iv
        for block in blocks:
            xor_result = xor(prev_ciphertext, block)
            curr_ciphertext = blackbox_encrypt(xor_result)
            ciphertext.append(curr_ciphertext)
            prev_ciphertext = curr_ciphertext
        return _bytes_to_string(b''.join(ciphertext))

    def decrypt(self, ciphertext):
        ciphertext = _string_to_bytes(ciphertext)
        return _bytes_to_string(blackbox_decrypt(ciphertext))

if len(sys.argv) != 3:
    print("Usage: python3 mode blocklength")
    sys.exit(1)

mode = sys.argv[1]
blocklength = int(sys.argv[2])
hallo = "hello world"
key = "hello world"
modeClass = None


if mode == "ecb":
    modeClass = modeECB()
elif mode == "cbc":
    modeClass = modeCBC("00000000")
else:
    print("Mode not supported")
    sys.exit(1)

print(modeClass.encrypt(hallo, blocklength))
print(modeClass.decrypt(modeClass.encrypt(hallo, blocklength)))
