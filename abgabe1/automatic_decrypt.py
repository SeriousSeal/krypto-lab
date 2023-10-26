import sys
import collections

#decrypt the file by subtracting the key from the ascii value of the character
def decrypt(data, key):
    decrypted_data = ""
    for char in data:
        if ord(char) >= 65 and ord(char) <= 90:
            decrypted_data += chr((ord(char) - 65 - key) % 26 + 65)
        else:
            decrypted_data += char

    return decrypted_data

# Count the frequency of each letter in the input data with collections and
# determine the most frequent letter assume the most frequent letter in the
# input data corresponds to the most frequent letter in the german language (which is 'E')
def crack_additive_cipher(data):
    letter_counts = collections.Counter(data)
    most_frequent_letter = letter_counts.most_common(1)[0][0]
    key = (ord(most_frequent_letter) - ord('E')) % 26
    decrypted_data = decrypt(data, key)
    return decrypted_data

if len(sys.argv) != 3:
    print("Usage: python3 automatic_decrypt.py <input_file> <output_file>")
    sys.exit(1)

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Open input file for reading
with open(input_file_name, 'r') as enryptedText:
    input_data = enryptedText.read()

decrypted_data = crack_additive_cipher(input_data)

# Open output file for writing
with open(output_file_name, 'w') as output_file:
    output_file.write(decrypted_data)