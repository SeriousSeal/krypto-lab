import sys
import re
from collections import Counter

def calculate_coincidence_index(text):
    # dictionary with { keys : the unique characters in the text ; values : counts of each character}
    freqs = Counter(text)
    #sum of the products of each freqency and one less than that frequency
    sum_freqs = sum(val*(val-1) for val in freqs.values())
    index = sum_freqs / (len(text)*(len(text)-1))
    return index

def key_length_analysis(text, max_key_length=100):
    
    # Initialize a list to store coincidence indices
    coincidence_indices = []
    
    # Loop over possible key lengths
    for i in range(1, max_key_length + 1):
        # divides the text into i pats, each part containing every ith character starting from a different position
        subtexts = [text[j::i] for j in range(i)]
        # calculates the average index of coincience
        avg_coincidence_index = sum(calculate_coincidence_index(subtext) for subtext in subtexts) / i
        coincidence_indices.append(avg_coincidence_index)

    # Find the key length with the highest coincidence index
    maxKey = max(coincidence_indices)
    result = [key for key in coincidence_indices if key >= 0.8 * maxKey]
    # possible to check also other keylengths
    estimated_key_length = coincidence_indices.index(result[0]) + 1
    return estimated_key_length


def determine_key(text):
    # Initialize the key with empty string
    key = ''    
    # we ignore every other chars except A-Z
    cleanedText = re.sub('[^A-Z]', '', text)
    keyLength = key_length_analysis(cleanedText)

    # Split the ciphertext into subtexts of 3 chars
    subtexts = [cleanedText[i::keyLength] for i in range(keyLength)]

    # For each subtext, find the character with the highest frequency
    for subtext in subtexts:
        freqs = Counter(subtext)
        max_freq_char = max(freqs, key=freqs.get)
        key += chr((ord(max_freq_char) - ord('E')) % 26 + 65)
    return key

# Input: text (the encrypted text) and keys (the decryption keys as ascii chars)
# It calculates the length of the key and conerts each character in the key to its ASCII value,
# storing these values in the list key_as_int
# same for the encrypted text as int
# loop: If the character is an uppercase letter, it encrypts it using the Vigenère cipher algorithm:
# it subtracts the ASCII value of the character and the corresponding ASCII value from the key
# takes the result modulo 26
def decrypt(text, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    encrypted_data = ''
    charCount = 0
    for char in text:
        if ord(char) >= 65 and ord(char) <= 90:
            value = (ord(char) - key_as_int[charCount % key_length]) % 26
            encrypted_data += chr(value + 65)
            charCount = charCount + 1
        else:
            encrypted_data += char
    return encrypted_data


# Check if correct number of arguments were provided
if len(sys.argv) != 3:
    print("Usage: python3 decrypt_vigenere.py <input_file> <output_file>")
    sys.exit(1)

# Get input file name, key, and output file name from command line arguments
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Open input file for reading
with open(input_file_name, 'r') as enryptedText:
    input_data = enryptedText.read()

key = determine_key(input_data)
decrypted_data = decrypt(input_data, key)

# Open output file for writing
with open(output_file_name, 'w') as output_file:
    output_file.write(decrypted_data)