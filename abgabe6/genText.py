import sys
import random

# Generate a file with random hex codes
def generate_hex_codes(num_times):
    str = ""
    for _ in range(num_times):
        hex_code = ''.join(random.choices('0123456789abcdef', k=4))
        str += hex_code + "\n"
    return str
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 genText.py <filename> <number of Texts>")
        sys.exit(1)
    
    filename = sys.argv[1]
    numText = int(sys.argv[2])
    
    hexStr = generate_hex_codes(numText)
    
    with open(filename, 'w') as f:
        f.write(hexStr)
        f.close()

