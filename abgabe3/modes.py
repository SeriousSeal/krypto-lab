import sys

# Pad the plaintext with zeros and convert it to a binary string
def _padAndByte(plaintext, blocklength):
    plaintext = _string_to_binary(plaintext)
    if len(plaintext) % blocklength != 0:
        toAddZeros = blocklength - len(plaintext) % blocklength
        plaintext += '0' * toAddZeros
    return plaintext

# Convert a binary string to a string
def _binary_to_string(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

# Convert a string to a binary string
def _string_to_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

# XOR two binary strings
def xor(a, b):
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

# Add two binary strings
def add(a, b):
    return bin(int(a, 2) + int(b, 2))[2:].zfill(8)
    
# "encrypt" algorithm
def blackbox_encrypt(byteString):
    return xor(byteString, key)

# "decrypt" algorithm
def blackbox_decrypt(byteString):
    return xor(byteString, key)

# Increment the counter
def counter_increment(counter):
    if(counter[-1] == '1'):
        return counter[1:] + "0"
    else:
        return counter[:-1] + "1"
    
# Implement the modes of operation
class modeECB():
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        for block in blocks:
            curr_ciphertext = blackbox_encrypt(block)
            ciphertext.append(curr_ciphertext)
        return ''.join(ciphertext)

    def decrypt(self, ciphertext, blocklength):
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)] 
        plaintext = []
        for block in blocks:
            decrypted = blackbox_decrypt(block)
            plaintext.append(decrypted)
        return _binary_to_string("".join(plaintext)) 

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
        return ''.join(ciphertext)

    def decrypt(self, ciphertext, blocklength):
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)] 
        plaintext = []
        prev_ciphertext = self.iv
        for block in blocks:
            decrypted = blackbox_decrypt(block)
            xor_result = xor(prev_ciphertext, decrypted)
            plaintext.append(xor_result)
            prev_ciphertext = block
        return _binary_to_string("".join(plaintext)) 

class modeOFB():
    def __init__(self, iv):
        self.iv = iv
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        prev_ciphertext = self.iv
        for block in blocks:            
            curr_ciphertext = blackbox_encrypt(prev_ciphertext)            
            prev_ciphertext = curr_ciphertext
            xor_result = xor(curr_ciphertext, block)
            ciphertext.append(xor_result)
        return ''.join(ciphertext)

    def decrypt(self, ciphertext, blocklength):
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]
        plaintext = []
        prev_ciphertext = self.iv
        for block in blocks:            
            curr_ciphertext = blackbox_encrypt(prev_ciphertext)            
            prev_ciphertext = curr_ciphertext
            xor_result = xor(curr_ciphertext, block)
            plaintext.append(xor_result)
        return  _binary_to_string("".join(plaintext))
    
class modeCTR():
    def __init__(self, iv, counter):
        self.counter = counter
        self.iv = iv

    def encrypt(self, plaintext, blocklength):
        enc_Counter = add(self.counter, self.iv)
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        for block in blocks:
            curr_ciphertext = blackbox_encrypt(enc_Counter)
            xor_result = xor(curr_ciphertext, block)
            ciphertext.append(xor_result)
            enc_Counter = counter_increment(enc_Counter)
        return ''.join(ciphertext)

    def decrypt(self, ciphertext, blocklength):
        enc_Counter = add(self.counter, self.iv)
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]
        plaintext = []
        for block in blocks:
            curr_ciphertext = blackbox_encrypt(enc_Counter)
            xor_result = xor(curr_ciphertext, block)
            plaintext.append(xor_result)
            enc_Counter = counter_increment(enc_Counter)
        return _binary_to_string(''.join(plaintext))

key = "00110011"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 modes.py mode blocklength")
        sys.exit(1)

    mode = sys.argv[1]
    blocklength = int(sys.argv[2])
    hallo = "hello world"    
    modeClass = None


    if mode == "ecb":
        modeClass = modeECB()
    elif mode == "cbc":
        modeClass = modeCBC("00000000")
    elif mode == "ofb":
        modeClass = modeOFB("00000000")
    elif mode == "ctr":
        modeClass = modeCTR("00000000", "00000000")
    else:
        print("Mode not supported")
        sys.exit(1)
        
    print(modeClass.decrypt(modeClass.encrypt(hallo, blocklength), blocklength))
