import sys

# Read a file and remove spaces and newlines
def read_file_remove_spaces_newlines(filename):
    with open(filename, 'r') as file:
        data = file.read().replace(' ', '').replace('\n', '')
    return data

# Read a file and remove spaces and newlines
def read_hex_file(filename):
    with open(filename, 'r') as file:
        hex_strings = file.readlines()
    # Remove newline characters and any leading/trailing whitespace
    hex_strings = [line.strip() for line in hex_strings]
    # Split each string on spaces and flatten the list
    hex_strings = [item for sublist in hex_strings for item in sublist.split()]
    return hex_strings

# XOR strings
def xor(*args):
    return ''.join(str(sum(int(x) for x in bits) % 2) for bits in zip(*args))

# AND strings
def andOp(bin_str1, bin_str2):
    int1 = int(bin_str1, 2)
    int2 = int(bin_str2, 2)
    and_result = int1 & int2
    return bin(and_result)[2:].zfill(len(bin_str1))

# Convert a hex string to a binary string
def hex_to_bin(hex_string):
   return ''.join(format(int(char, 16), '04b') for char in hex_string)

# Calculate the quality of a linear approximation
def calculateQuality(U, V, approximation):
    T = 1
    for i in range(4):
        L = 0
        for j in range(16):            
            u = U[j]
            Ua = andOp(u, approximation[i][0:4])
            v = V[j]            
            Vb = andOp(v, approximation[i][4:8])
            if xor(Ua[0],Ua[1],Ua[2],Ua[3],Vb[0],Vb[1],Vb[2],Vb[3]) == "0":
                L += 1
        bias = (L - 8)/16
        T *= abs(bias)
    return T
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 checkQualityLinApprox.py <sbox_file> <approximation_file>")
        sys.exit(1)
        
    sbox_file = sys.argv[1]	
    approx_file = sys.argv[2]
    
    sbox = read_file_remove_spaces_newlines(sbox_file)
    
    V = [hex_to_bin(sbox[i]) for i in range(16)]
    U = [format(i, '04b') for i in range(16)]
    
    approximation = read_hex_file(approx_file)
    if any(approximation[i] == '00' for i in [1, 5, 9, 11]):
        print(-1)
        sys.exit(1)
        
    approximation = [hex_to_bin(approximation[i]) for i in [1, 5, 9, 11]]
    quality = calculateQuality(sbox, U, V, approximation)
    
    print(quality)