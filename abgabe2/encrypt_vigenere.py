import sys

# Input: text (the encrypted text) and keys (the decryption keys as ascii chars)
# It calculates the length of the key and conerts each character in the key to its ASCII value,
# storing these values in the list key_as_int
# same for the encrypted text as int
# loop: If the character is an uppercase letter, it encrypts it using the Vigenère cipher algorithm:
# it adds the ASCII value of the character and the corresponding ASCII value from the key
# takes the result modulo 26
def encrypt(text, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    encrypted_data = ''
    charCount = 0
    for char in text:
        if ord(char) >= 65 and ord(char) <= 90:
            value = (ord(char) + key_as_int[charCount % key_length]) % 26
            encrypted_data += chr(value + 65)
            charCount = charCount + 1
        else:
            encrypted_data += char
    return encrypted_data

if __name__ == "__main__":
    # Check if correct number of arguments were provided
    if len(sys.argv) != 4:
        print("Usage: python3 encrypt_vigenere.py <input_file> <keys> <output_file>")
        sys.exit(1)

    # Get input file name, key, and output file name from command line arguments
    input_file_name = sys.argv[1]
    key = sys.argv[2]
    output_file_name = sys.argv[3]

    # Open input file for reading
    with open(input_file_name, 'r') as enryptedText:
        input_data = enryptedText.read()

    encrypted_data = encrypt(input_data, key)

    # Open output file for writing
    with open(output_file_name, 'w') as output_file:
        output_file.write(encrypted_data)