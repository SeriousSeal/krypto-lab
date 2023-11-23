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

rcon =[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]

#
def GaloisMultiplication(number, multiplier):
   number_bin = format(number, '08b')
   if multiplier == 0x01:
      return number
   elif multiplier == 0x02:
      mask = 2 ** 8 - 1
      num_shifted = (number << 1) & mask
      if number_bin[0] == '1':
         return (num_shifted ^ 0b00011011)
      else:
         return num_shifted
   elif multiplier == 0x03:
      return (GaloisMultiplication(number, 0x02) ^ number)
   elif multiplier == 0x09:
      a = number
      for i in range(0, 3):
         a = GaloisMultiplication(a, 0x02)
      return (a ^ number)
   elif multiplier == 0x0b:
      a = number
      for i in range(0, 2):
         a = GaloisMultiplication(a, 0x02)
      a = a ^ number
      a = GaloisMultiplication(a, 0x02)
      return (a ^ number)
   elif multiplier == 0x0d:
      a = number
      a = GaloisMultiplication(a, 0x02)
      a = a ^ number
      for i in range(0, 2):
         a = GaloisMultiplication(a, 0x02)
      return (a ^ number)
   elif multiplier == 0x0e:
      a = number
      for i in range(0, 2):
         a = GaloisMultiplication(a, 0x02)
         a = a ^ number
      return (GaloisMultiplication(a, 0x02))
   
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
    
def SubBytesTransformation(matrix):
    new_matrix = deepcopy(matrix)

    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[0])):
            num_str = new_matrix[row][col]
            s_row, s_col = int(num_str[2], 16), int(num_str[3], 16)
            new_matrix[row][col] = "0x{:02x}".format(s_box[s_row][s_col])
    return new_matrix
 
def InvSubBytesTransformation(matrix):
    new_matrix = deepcopy(matrix)

    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[0])):
            num_str = new_matrix[row][col]
            s_row, s_col = int(num_str[2], 16), int(num_str[3], 16)
            new_matrix[row][col] = "0x{:02x}".format(inv_s_box[s_row][s_col])
    return new_matrix

def AddRoundKey(matrix, round_key):
    return [["0x{:02x}".format(int(matrix[row][col], 16) ^ int(round_key[row*4 + col], 16)) 
             for col in range(4)] for row in range(4)]

def generateRoundkeys(key_array):
    round_keys = key_array[0]

    for i in range(5,44):
        if i % 4 == 0:
            print (round_keys[i-1])
            word = rotWord(round_keys[i-1])
            print (word)
            word = subWord(word) if len(word) >= 4 else word
            word = "0x{:02x}".format(int(round_keys[i-4], 16) ^ rcon[int(i/4) - 1]) ^ word

            round_keys.append(word)
        else:
            round_keys.append("0x{:02x}".format(int(round_keys[i-4], 16) ^ int(round_keys[i-1], 16)))

    return round_keys

def rotWord(word):
   return word[1:] + word[:1]

def subWord(word):
   return "0x{:02x}".format(s_box[int(word[2], 16)][int(word[3], 16)])

def ShiftRows(matrix):
    for i in range(4):
        row = [matrix[j][i] for j in range(4)]
        row = row[i:] + row[:i]
        for j in range(4):
            matrix[j][i] = row[j]
    return matrix
 
def InvShiftRows(matrix):
    for i in range(4):
        row = [matrix[j][i] for j in range(4)]
        row = row[-i:] + row[:-i]
        for j in range(4):
            matrix[j][i] = row[j]
    return matrix
    
def AES_Encrypt(matrix, round_keys):
   new_matrix = deepcopy(matrix)
   round_keys = generateRoundkeys(round_keys)
   print(round_keys)
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

def AES_Decrypt(matrix: str, round_keys: str) -> str:
   new_matrix = deepcopy(matrix)
   round_keys = generateRoundkeys(round_keys)
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
            
def AES_Cipher(mode, input_matrix, key_matrix):
    if mode == 'encrypt':
        return AES_Encrypt(input_matrix, key_matrix)
    elif mode == 'decrypt':
        return AES_Decrypt(input_matrix, key_matrix)
    else:
        raise ValueError("Invalid mode. Expected 'encrypt' or 'decrypt'.")

if len(sys.argv) != 6 and len(sys.argv) != 5:
    print("Usage: python3 aes.py <modus> <input_file> <key_file> <output_file> ?<iv_file>")
    sys.exit(1)

mode = sys.argv[1]
input_file = sys.argv[2]
key_file_name = sys.argv[3]
output_file_name = sys.argv[4]
iv_file_name = sys.argv[5] if len(sys.argv) == 6 else None
if mode != 'ecb' and iv_file_name is  None:
   raise ValueError("Invalid mode. Expected iv file for this mode")

result_matrix = AES_Cipher('encrypt', read_matrixfile_into_matrix(input_file), read_file_into_matrix(key_file_name))
write_matrix_into_file(result_matrix, output_file_name)