import sys

sbox = ["1110","0100", "1101", "0001", "0010", "1111", "1011", "1000", "0011", "1010", "0110", "1100", "0101", "1001", "0000", "0111"]
inv_sbox = ['1110', '0011', '0100', '1000', '0001', '1100', '1010', '1111', '0111', '1101', '1001', '0110', '1011', '0010', '0000', '0101']
hexDigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

alpha = [0 for i in range(16**2)]

def read_file_remove_spaces_newlines(filename):
    with open(filename, 'r') as file:
        data = file.read().replace(' ', '').replace('\n', '')
    return data

def hex_to_binary(hex_string):
    binary_string = bin(int(hex_string, 16))[2:]
    return binary_string.zfill(len(hex_string) * 4)

def binary_to_hex(binary_string):
    hex_string = hex(int(binary_string, 2))[2:]
    return hex_string

def xor(*args):
    xor_result = 0
    for arg in args:
        xor_result ^= int(arg, 2)
    return bin(xor_result)[2:]


def binary_to_int(binary: str) -> int:
    return int(binary, 2)

partialKeys = [(hex_to_binary(i),hex_to_binary(j)) for i in hexDigits for j in hexDigits]

def getMaxKey(M):
    for (a,b) in M:
        for (L1, L2) in partialKeys:
            v2 = xor(L1, b[4:8])
            v4 = xor(L2, b[12:16])
            u2 = inv_sbox[binary_to_int(v2)]
            u4 = inv_sbox[binary_to_int(v4)]
            if xor(a[4],a[6],a[7],u2[1],u2[3],u4[1],u4[3]) == "0":
                alpha[binary_to_int(L1)+ binary_to_int(L2)*16] += 1
    maxval = -1
    for (L1, L2) in partialKeys:
        beta = abs(alpha[binary_to_int(L1)+ binary_to_int(L2)*16] - len(M)/2)
        if beta > maxval:
            maxval = beta
            maxkey = (L1, L2)
    return maxkey

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 linAttack.py <input_textfile> <cipher_textfile> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    cipher_file = sys.argv[2]
    output_file = sys.argv[3]
    input_text = read_file_remove_spaces_newlines(input_file)
    input_array = [hex_to_binary(input_text[i:i+4]) for i in range(0, len(input_text), 4)]

    cipher_text = read_file_remove_spaces_newlines(cipher_file)
    cipher_array = [hex_to_binary(cipher_text[i:i+4]) for i in range(0, len(cipher_text), 4)]

    #plain and cipher text pairs
    M = [(input_array[i], cipher_array[i]) for i in range(len(input_array))]

    maxkey = getMaxKey(M)

    with open(output_file, 'w') as f:
        f.write(binary_to_hex(maxkey[0]+maxkey[1]))
        
if __name__ == '__main__':
    main()