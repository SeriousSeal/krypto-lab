import sys

s_box = ['e', '4', 'd', '1', '2', 'f', 'b', '8', '3', 'a', '6', 'c', '5', '9', '0', '7']
permutation = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]

def read_file_remove_spaces_newlines(filename):
    with open(filename, 'r') as file:
        data = file.read().replace(' ', '').replace('\n', '')
    return data

def xor(a:str, b:str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

def write_array_into_file(array, filename):
    with open(filename, 'w') as file:
        file.write(' '.join(array))
    
def _hex_to_bin(hex_string):
   return ''.join(format(int(char, 16), '04b') for char in hex_string)

def _binary_to_hex(block):
    return hex(int(block, 2))[2:].zfill(len(block) // 4)

def permute(block):
    return ''.join(block[permutation[i]-1] for i in range(len(block)))

def substitute(block):
    return _hex_to_bin(''.join(s_box[int(block[i:i+4], 2)] for i in range(0, len(block), 4)))

def spn(input:str, key:str) -> str:
    input = _hex_to_bin(input)    
    key = _hex_to_bin(key)
    for i in range(3):
        input = xor(input, key)
        input = substitute(input)
        input = permute(input)
    input = xor(input, key)
    input = substitute(input)
    input = xor(input, key)
    return input

if len(sys.argv) != 4:
    print("Usage: python3 spn.py <input> <key> <output>")
    sys.exit(1)
    
input_file = sys.argv[1]
key_file = sys.argv[2]
output_file = sys.argv[3]

key_text = read_file_remove_spaces_newlines(key_file)

output_array = []
input_text = read_file_remove_spaces_newlines(input_file)
input_array = [input_text[i:i+4] for i in range(0, len(input_text), 4)]
for i in range(len(input_array)):
    output_array.append(_binary_to_hex(spn(input_array[i], key_text)))

write_array_into_file(output_array, output_file)
    