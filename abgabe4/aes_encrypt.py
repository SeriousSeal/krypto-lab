from copy import deepcopy
import sys
from s_box import s_box
from s_box import inv_s_box


# AES MixColumns Matrix
aes_matrix = [[0x02,0x03,0x01,0x01],
              [0x01,0x02,0x03,0x01],
              [0x01,0x01,0x02,0x03],
              [0x03,0x01,0x01,0x02]]

# Funktion für Galois-Multiplikation
def galois_multiply(a, b):
    product = 0
    for _ in range(8):
        if b & 1: 
            product ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit: 
            a ^= 0x1b
        b >>= 1
    return product

# Funktion für MixColumns in AES
def MixColumns(state):
    temp_state = [[0, 0, 0, 0] for _ in range(4)]
    for col in range(4):
        for row in range(4):
            temp_state[row][col] = 0
            for k in range(4):
                temp_state[row][col] ^= galois_multiply(aes_matrix[row][k], int(state[k][col], 16))
    return [["0x{:02x}".format(num) for num in row] for row in temp_state]
    
def SubBytesTransformation(matrix):
    new_matrix = deepcopy(matrix)

    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[0])):
            num_str = new_matrix[row][col]
            s_row, s_col = int(num_str[2], 16), int(num_str[3], 16)
            new_matrix[row][col] = "0x{:02x}".format(s_box[s_row][s_col])

    return new_matrix

def AddRoundKey(matrix, round_key):
    return [["0x{:02x}".format(int(matrix[row][col], 16) ^ int(round_key[row*4 + col], 16)) 
             for col in range(4)] for row in range(4)]
    

def ShiftRows(matrix):
    return [matrix[i][i:] + matrix[i][:i] if i else matrix[i] for i in range(4)]
    
    
def AES_Encrypt(matrix, round_keys):
   new_matrix = deepcopy(matrix)
   new_matrix = AddRoundKey(new_matrix, round_keys[0])
   for i in range(1, 10):
      new_matrix = SubBytesTransformation(new_matrix)
      new_matrix = ShiftRows(new_matrix)
      new_matrix = MixColumns(new_matrix)
      new_matrix = AddRoundKey(new_matrix, round_keys[i])

   new_matrix = SubBytesTransformation(new_matrix)
   new_matrix = ShiftRows(new_matrix)
   new_matrix = AddRoundKey(new_matrix, round_keys[10])

   return new_matrix

def read_file_into_matrix(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    matrix = [[byte for byte in line.strip().split()] for line in lines]
    return matrix

def read_matrixfile_into_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        data = file.read().split()
        for i in range(0, len(data), 4):
            row = data[i:i+4]
            matrix.append(row)
    return matrix

def write_matrix_into_file(matrix, file_name):
    with open(file_name, 'w') as file:
        for row in matrix:
            file.write(" ".join(row).replace("0x", "") + " ")

if len(sys.argv) != 5 and len(sys.argv) != 6:
    print("Usage: python3 aes_encrypt.py <Betriebsmodus> <input_file> <key_file> <output_file> ?optional: <iv>")
    sys.exit(1)

mode = sys.argv[1]
input_file = sys.argv[2]
key_file_name = sys.argv[3]
output_file_name = sys.argv[4]
iv = sys.argv[5] if len(sys.argv) == 6 else None

input_matrix = read_matrixfile_into_matrix(input_file)
key_matrix = read_file_into_matrix(key_file_name)

encrypted_Matrix = AES_Encrypt(input_matrix, key_matrix)
write_matrix_into_file(encrypted_Matrix, output_file_name)
