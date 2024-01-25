import sys

#encrypt the file by adding the key to the ascii value of the character
def encrypt(data, key):
    encrypted_data = ""
    for char in data:
        if ord(char) >= 65 and ord(char) <= 90:
            encrypted_data += chr((ord(char) - 65 + int(key)) % 26 + 65)
        else:
            encrypted_data += char

    return encrypted_data

# Check if correct number of arguments were provided

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encrypt_add_chiffre.py <input_file> <key> <output_file>")
        sys.exit(1)
    
    # Get input file name, key, and output file name from command line arguments
    input_file_name = sys.argv[1]
    key = sys.argv[2]
    output_file_name = sys.argv[3]
    
    # Open input file for reading
    with open(input_file_name, 'r') as plaintext:
        input_data = plaintext.read()
    
    encrypted_data = encrypt(input_data, key)
    
    # Open output file for writing
    with open(output_file_name, 'w') as output_file:
        output_file.write(encrypted_data)