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

rcon =[[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36],
       [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
       [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
       [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]]

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
   round_keys = []
   for i in range(0, 16, 4):
      row = key_array[0][i:i+4]
      round_keys.append(row)      
   for i in range(4,44):
      if i % 4 == 0:
         word = rotWord(round_keys[i-1])
         word = subWord(word)
         word = ["{:02x}".format(int(round_keys[i-4][j], 16) ^ rcon[j][int(i/4) - 1] ^ int(word[j], 16)) for j in range(4)]
         round_keys.append(word)
      else:
         round_keys.append(["{:02x}".format(int(round_keys[i-4][j], 16) ^ int(round_keys[i-1][j], 16)) for j in range(4)])
   reshaped_round_keys = reshape_round_keys(round_keys)
   return reshaped_round_keys

def rotWord(word):
   return word[1:] + word[:1]

def subWord(word):
   word = ["{:02x}".format(s_box[int(byte[0], 16)][int(byte[1], 16)]) for byte in word]
   return word

def reshape_round_keys(round_keys):
    reshaped_round_keys = []
    for i in range(11):  # We have 11 columns in the reshaped matrix
        column = []
        for j in range(4):  # Each column is formed by 4 consecutive keys
            for k in range(4):  # Each key has 4 elements
                column.append(round_keys[j + i*4][k])
        reshaped_round_keys.append(column)
    return reshaped_round_keys

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

def write_multiple_matrices_into_file(matrices, file_name):
    with open(file_name, 'w') as file:
         for matrix in matrices:
            for row in matrix:
              file.write(" ".join(row).replace("0x", "") + " ")
            file.write("\n")
                        
def AES_Cipher(mode, input_matrix, key_matrix):
   if mode == 'encrypt':
       return AES_Encrypt(input_matrix, key_matrix)
   elif mode == 'decrypt':
       return AES_Decrypt(input_matrix, key_matrix)
   else:
       raise ValueError("Invalid mode. Expected 'encrypt' or 'decrypt'.")

def _padAndByte(plaintext, blocklength):
   plaintext = _hex_to_bin(plaintext)
   if len(plaintext) % blocklength != 0:
       toAddZeros = blocklength - len(plaintext) % blocklength
       plaintext += '0' * toAddZeros
   return plaintext   
 
def _bin_to_hex(b):
   return ''.join(hex(int(b[i:i+8], 2))[2:].zfill(2) for i in range(0, len(b), 8))

def _hex_to_bin(hex_string):
   return ''.join(format(int(char, 16), '04b') for char in hex_string)
 
def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

def binary_to_hex(block):
    return hex(int(block, 2))[2:].zfill(len(block) // 4)

def matrix_bin_to_hex(matrix):
    return [[binary_to_hex(cell) for cell in row] for row in matrix]

def block_to_matrix(block):
    bin_matrix = [[block[j+i:j+i+8] for i in range(0, 32, 8)] for j in range(0, 128, 32)]
    return matrix_bin_to_hex(bin_matrix)

def matrix_to_bit_string(matrix):
    return ''.join(''.join(format(int(cell, 16), '08b') for cell in row) for row in matrix)

def hexStr_to_binaryStr(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

def read_file_remove_spaces_newlines(filename):
    with open(filename, 'r') as file:
        data = file.read().replace(' ', '').replace('\n', '')
    return data

def add_binary_nums(a, b):
    sum_bin = bin(int(a, 2) + int(b, 2))[2:]
    max_length = max(len(a), len(b))
    return sum_bin.zfill(max_length)
    
class modeECB():
    def __init__(self, key_file_name):
        self.key_file_name = key_file_name
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        for block in blocks:
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(block), read_file_into_matrix(self.key_file_name))
            ciphertext.append(curr_ciphertext)        
        return ciphertext

    def decrypt(self, ciphertext, blocklength):
        ciphertext = _hex_to_bin(ciphertext)
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]  # Split the ciphertext into blocks
        plaintext = []
        for block in blocks:
            decrypted = AES_Cipher('decrypt', block_to_matrix(block), read_file_into_matrix(self.key_file_name))
            plaintext.append(decrypted)
        return plaintext

class modeCBC():
    def __init__(self, iv, key_file_name):
        self.iv = iv
        self.key_file_name = key_file_name
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        prev_ciphertext = hexStr_to_binaryStr(self.iv)
        for block in blocks:
            xor_result = xor(prev_ciphertext, block)
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(xor_result), read_file_into_matrix(self.key_file_name))
            ciphertext.append(curr_ciphertext)
            prev_ciphertext = matrix_to_bit_string(curr_ciphertext)
        return ciphertext

    def decrypt(self, ciphertext, blocklength):
        ciphertext = _hex_to_bin(ciphertext)
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]  # Split the ciphertext into blocks
        plaintext = []
        prev_ciphertext = hexStr_to_binaryStr(self.iv)
        for block in blocks:
            decrypted = AES_Cipher('decrypt', block_to_matrix(block), read_file_into_matrix(self.key_file_name))
            xor_result = xor(prev_ciphertext, matrix_to_bit_string(decrypted))
            plaintext.append(block_to_matrix(xor_result))
            prev_ciphertext = block
        return plaintext  # Convert binary strings to integers before passing to _binary_to_string

class modeOFB():
    def __init__(self, iv, key_file_name):
        self.iv = iv
        self.key_file_name = key_file_name
    def encrypt(self, plaintext, blocklength):
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        prev_ciphertext = hexStr_to_binaryStr(self.iv)
        for block in blocks:       
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(prev_ciphertext), read_file_into_matrix(self.key_file_name))
            prev_ciphertext = matrix_to_bit_string(curr_ciphertext)
            xor_result = xor(matrix_to_bit_string(curr_ciphertext), block)
            ciphertext.append(block_to_matrix(xor_result))
        return ciphertext

    def decrypt(self, ciphertext, blocklength):
        ciphertext = _hex_to_bin(ciphertext)
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]
        plaintext = []
        prev_ciphertext = hexStr_to_binaryStr(self.iv)
        for block in blocks:
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(prev_ciphertext), read_file_into_matrix(self.key_file_name))  # Change 'decrypt' to 'encrypt'
            prev_ciphertext = matrix_to_bit_string(curr_ciphertext)
            xor_result = xor(matrix_to_bit_string(curr_ciphertext), block)
            plaintext.append(block_to_matrix(xor_result))
        return plaintext
    
class modeCTR():
    def __init__(self, iv, counter, key_file_name):
        self.counter = counter
        self.iv = iv
        self.key_file_name = key_file_name

    def encrypt(self, plaintext, blocklength):
        self.iv = hexStr_to_binaryStr(self.iv)        
        self.counter = hexStr_to_binaryStr(self.counter)
        enc_Counter = add_binary_nums(self.counter, self.iv)
        plaintext = _padAndByte(plaintext, blocklength)
        blocks = [plaintext[i:i+blocklength] for i in range(0, len(plaintext), blocklength)]
        ciphertext = []
        for block in blocks:
            print(enc_Counter)
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(enc_Counter), read_file_into_matrix(self.key_file_name))
            xor_result = xor(matrix_to_bit_string(curr_ciphertext), block)
            ciphertext.append(block_to_matrix(xor_result))
            enc_Counter = counter_increment(enc_Counter)  # Increment the counter
        return ciphertext

    def decrypt(self, ciphertext, blocklength):
        self.iv = hexStr_to_binaryStr(self.iv)
        self.counter = hexStr_to_binaryStr(self.counter)
        enc_Counter = add_binary_nums(self.counter, self.iv)
        ciphertext = _hex_to_bin(ciphertext)
        blocks = [ciphertext[i:i+blocklength] for i in range(0, len(ciphertext), blocklength)]
        plaintext = []
        for block in blocks:
            curr_ciphertext = AES_Cipher('encrypt', block_to_matrix(enc_Counter), read_file_into_matrix(self.key_file_name))  # Encrypt the counter
            xor_result = xor(matrix_to_bit_string(curr_ciphertext), block)
            plaintext.append(block_to_matrix(xor_result))
            enc_Counter = counter_increment(enc_Counter)  # Increment the counter
        return plaintext

def counter_increment(counter):
    if(counter[-1] == '1'):
        return counter[1:] + "0"
    else:
        return counter[:-1] + "1"