import sys

def read_file_remove_spaces_newlines(filename):
    with open(filename, 'r') as file:
        data = file.read().replace(' ', '').replace('\n', '')
    return data

def calculate_u4_bits(plaintext, ciphertext):
    # Convert hexadecimal strings to integers
    plaintext_int = int(plaintext, 16)
    ciphertext_int = int(ciphertext, 16)
    # Perform XOR operation
    u4 = plaintext_int ^ ciphertext_int
    # Extract the required bits from u4
    u4_bits = (u4 >> 5 & 1, u4 >> 7 & 1, u4 >> 8 & 1, u4 >> 6 & 1, u4 >> 8 & 1, u4 >> 14 & 1, u4 >> 16 & 1)
    return u4_bits

def calculate_approximation_probability(u4_bits, L1, L2):
    L1_bit = (L1 >> 2) & 1
    L2_bit = (L2 >> 2) & 1
    Ua = u4_bits[0] ^ u4_bits[1] ^ u4_bits[2] ^ L1_bit
    Vb = u4_bits[3] ^ u4_bits[4] ^ u4_bits[5] ^ u4_bits[6] ^ L2_bit
    approximation_holds = Ua == Vb
    return approximation_holds

def linear_analysis(plaintexts, ciphertexts):
    L1_candidates = [i for i in range(16)]
    L2_candidates = [i for i in range(16)]
    results = []
    for L1 in L1_candidates:
        for L2 in L2_candidates:
            count = 0
            for plaintext, ciphertext in zip(plaintexts, ciphertexts):
                u4_bits = calculate_u4_bits(plaintext, ciphertext)
                if calculate_approximation_probability(u4_bits, L1, L2):
                    count += 1
            probability = count / len(plaintexts)
            bias = abs(probability - 0.5)
            results.append((bin(L1)[2:].zfill(4), bin(L2)[2:].zfill(4), bias))
    if results:
        print(results)
        best_candidate = max(results, key=lambda x: x[2])
        return best_candidate
    else:
        return "no result found"


if len(sys.argv) != 4:
    print("Usage: python3 linAttack.py <input_textfile> <cipher_textfile> <output_file>")
    sys.exit(1)
    
input_file = sys.argv[1]
cipher_file = sys.argv[2]
output_file = sys.argv[3]
input_text = read_file_remove_spaces_newlines(input_file)
input_array = [input_text[i:i+4] for i in range(0, len(input_text), 4)]

cipher_text = read_file_remove_spaces_newlines(cipher_file)
cipher_array = [cipher_text[i:i+4] for i in range(0, len(cipher_text), 4)]

results = linear_analysis(input_array, cipher_array)

print(results)

with open(output_file, 'w') as file:
    file.write(', '.join(map(str, results)))