from copy import deepcopy
import sys
from s_box import s_box
from s_box import inv_s_box


mix_column_matrix = [[0x02,0x03,0x01,0x01],
                     [0x01,0x02,0x03,0x01],
                     [0x01,0x01,0x02,0x03],
                     [0x03,0x01,0x01,0x02]]

inv_mix_column_matrix = [[0x0e, 0x0b, 0x0d, 0x09],
                         [0x09, 0x0e, 0x0b, 0x0d],
                         [0x0d, 0x09, 0x0e, 0x0b],
                         [0x0b, 0x0d, 0x09, 0x0e]]

# Galois Multiplication
def GaloisMultiplication(number, multiplier):    
    if multiplier == 0x01:
        return number
    elif multiplier == 0x02:
        return galois_multiply_by_02(number)
    elif multiplier == 0x03:
        return galois_multiply_by_03(number)
    elif multiplier == 0x09:
        return galois_multiply_by_09(number)
    elif multiplier == 0x0b:
        return galois_multiply_by_0b(number)
    elif multiplier == 0x0d:
        return galois_multiply_by_0d(number)
    elif multiplier == 0x0e:
        return galois_multiply_by_0e(number)

def galois_multiply_by_02(number):
    mask = 2 ** 8 - 1
    num_shifted = (number << 1) & mask
    if number & 0x80:
        return (num_shifted ^ 0b00011011)
    else:
        return num_shifted

def galois_multiply_by_03(number):
    return (galois_multiply_by_02(number) ^ number)

def galois_multiply_by_09(number):
    result = number
    for _ in range(0, 3):
        result = galois_multiply_by_02(result)
    return (result ^ number)

def galois_multiply_by_0b(number):
    result = number
    for _ in range(0, 2):
        result = galois_multiply_by_02(result)
    result ^= number
    result = galois_multiply_by_02(result)
    return (result ^ number)

def galois_multiply_by_0d(number):
    result = galois_multiply_by_02(number)
    result ^= number
    for _ in range(0, 2):
        result = galois_multiply_by_02(result)
    return (result ^ number)

def galois_multiply_by_0e(number):
    result = number
    for _ in range(0, 2):
        result = galois_multiply_by_02(result)
        result ^= number
    return galois_multiply_by_02(result)
 
# Inverse Mix Columns
def InvMixColumns(matrix):
   new_matrix = deepcopy(matrix)
   for c in range(4):
      new_column = [0,0,0,0]
      for row in range(4):
         for col in range(4):
            element = int(matrix[c][col], 16)
            new_column[row] ^= GaloisMultiplication(element, inv_mix_column_matrix[row][col])
      for r in range(4):
         new_matrix[c][r] = "0x{:02x}".format(new_column[r])
      
   return new_matrix
# Mix Columns
def MixColumns(matrix):
   new_matrix = deepcopy(matrix)
   for c in range(4):
      new_column = [0,0,0,0]
      for row in range(4):
         for col in range(4):
            element = int(matrix[c][col], 16)
            new_column[row] ^= GaloisMultiplication(element, mix_column_matrix[row][col])
      for r in range(4):
         new_matrix[c][r] = "0x{:02x}".format(new_column[r])
   return new_matrix

# Sub Bytes Transformation
def SubBytesTransformation(matrix):
    new_matrix = deepcopy(matrix)

    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[0])):
            num_str = new_matrix[row][col]
            s_row, s_col = int(num_str[2], 16), int(num_str[3], 16)
            new_matrix[row][col] = "0x{:02x}".format(s_box[s_row][s_col])
    return new_matrix

#  Inverse Sub Bytes Transformation
def InvSubBytesTransformation(matrix):
    new_matrix = deepcopy(matrix)

    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[0])):
            num_str = new_matrix[row][col]
            s_row, s_col = int(num_str[2], 16), int(num_str[3], 16)
            new_matrix[row][col] = "0x{:02x}".format(inv_s_box[s_row][s_col])
    return new_matrix

# Add Round Key
def AddRoundKey(matrix, round_key):
    return [["0x{:02x}".format(int(matrix[row][col], 16) ^ int(round_key[row*4 + col], 16)) 
             for col in range(4)] for row in range(4)]
    
# Shift Rows
def ShiftRows(matrix):
    for i in range(4):
        row = [matrix[j][i] for j in range(4)]
        row = row[i:] + row[:i]
        for j in range(4):
            matrix[j][i] = row[j]
    return matrix
 
# Inverse Shift Rows
def InvShiftRows(matrix):
    for i in range(4):
        row = [matrix[j][i] for j in range(4)]
        row = row[-i:] + row[:-i]
        for j in range(4):
            matrix[j][i] = row[j]
    return matrix

# AES ENcrypt
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

# AES Decrypt
def AES_Decrypt(matrix: str, round_keys: str) -> str:
   new_matrix = deepcopy(matrix)    
   new_matrix = AddRoundKey(new_matrix, round_keys[10])
   for i in range(9, 0, -1):
      new_matrix = InvShiftRows(new_matrix)
      new_matrix = InvSubBytesTransformation(new_matrix)
      new_matrix = AddRoundKey(new_matrix, round_keys[i])
      new_matrix = InvMixColumns(new_matrix)
   new_matrix = InvSubBytesTransformation(new_matrix)
   new_matrix = InvShiftRows(new_matrix)
   new_matrix = AddRoundKey(new_matrix, round_keys[0])
   return new_matrix

# Read file into matrix
def read_file_into_matrix(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    matrix = [[byte for byte in line.strip().split()] for line in lines]
    return matrix

# Read matrixfile into matrix
def read_matrixfile_into_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        data = file.read().split()
        for i in range(0, len(data), 4):
            row = data[i:i+4]
            matrix.append(row)
    return matrix
 
# Write matrix into file
def write_matrix_into_file(matrix, file_name):
    with open(file_name, 'w') as file:
        for row in matrix:
            file.write(" ".join(row).replace("0x", "") + " ")

# AES Cipher running mode         
def AES_Cipher(mode, input_matrix, key_matrix):
    if mode == 'encrypt':
        return AES_Encrypt(input_matrix, key_matrix)
    elif mode == 'decrypt':
        return AES_Decrypt(input_matrix, key_matrix)
    else:
        raise ValueError("Invalid mode. Expected 'encrypt' or 'decrypt'.")

if __name__ == '__main__':
   if len(sys.argv) != 5 and len(sys.argv) != 5:
       print("Usage: python3 aes.py encrypt/decrypt <input_file> <key_file> <output_file> ")
       sys.exit(1)
   
   mode = sys.argv[1]
   input_file = sys.argv[2]
   key_file_name = sys.argv[3]
   output_file_name = sys.argv[4]
   
   result_matrix = AES_Cipher(mode, read_matrixfile_into_matrix(input_file), read_file_into_matrix(key_file_name))
   write_matrix_into_file(result_matrix, output_file_name)