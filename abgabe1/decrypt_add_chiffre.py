import sys
import math

#decrypt the file by subtracting the key from the ascii value of the character
def decrypt(data, key):
    decrypted_data = ""
    for char in data:
        if ord(char) >= 65 and ord(char) <= 90:
            decrypted_data += chr((ord(char) - 65 - key) % 26 + 65)
        else:
            decrypted_data += char

    return decrypted_data

# Check if correct number of arguments were provided
if len(sys.argv) != 4:
    print("Usage: python3 decrypt_add_chiffre.py <input_file> <key> <output_file>")
    sys.exit(1)

# Get input file name, key, and output file name from command line arguments
input_file_name = sys.argv[1]
key = int(sys.argv[2])
output_file_name = sys.argv[3]

# Open input file for reading
with open(input_file_name, 'r') as enryptedText:
    input_data = enryptedText.read()

decrypted_data = decrypt(input_data, key)

# Open output file for writing
with open(output_file_name, 'w') as output_file:
    output_file.write(decrypted_data)