import sys
import re

# xor function for arbitrary number of bit strings
def _xor(*args):
    return ''.join(str(sum(int(b) for b in bits) % 2) for bits in zip(*args))

# calculate coordinates in a strided string array
# offset of i + offset of j + offset of k
def _calculate_coordinates(i, j, k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + 63 - (k % 64)

# converts bin string to hex string
def _bin_to_hex(b):
    return ''.join(''.join([hex(int(b[i:i+4], 2))[2:]]) for i in range(0, len(b), 4))

# converts hex string to bin string
def _hex_to_bin(hex_string):
    hex_string = re.sub(r"[^A-Fa-f0-9]", '', hex_string)
    return ''.join(format(int(char, 16), '04b') for char in hex_string)

# calculates parity
def _parity(A, j, k, dimension_size):
    column_indices = [_calculate_coordinates(i, j, k) for i in range(dimension_size)]
    return _xor(*[A[idx] for idx in column_indices])

def _pad(N, r):
    N += "1"
    padded = []
    while len(N) % (r-1) != 0:
        N += "0"
    N += "1"
    for i in range(0, len(N), r):
        padded.append(N[i:i+r])
    return padded

# implement theta
def theta(A):
    out = []
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out.append(_xor(A[_calculate_coordinates(i, j, k)], _parity(A, j-1, k, 5), _parity(A, j+1, k-1, 5)))
    return ''.join(out)
    

# next submission
def pi(A):
    return A

# next submission
def chi(A):
    return A

# next submission
def iota(A):
    return A

# next submission
def rho(A):
    return A

def f(A, rounds):
    for _ in range(rounds):
        A = theta(A)
        A = rho(A)
        A = pi(A)
        A = chi(A)
        A = iota(A)
    
    return A

def sha3(str, b, c, d, r, rounds):
    blocks = _pad(str, r)
    state = "0" * b
    for block in blocks:
        state = _xor(state, block+("0"*c))
        state = f(state, rounds)
    return state[0:d]


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python sha3.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    rounds = 24
    d = 224
    r = 1152
    c = 448
    b = c+r

    with open(input_file, "r") as file:
        data = _hex_to_bin(file.read())

    with open(output_file, "w") as file:
        file.write(_bin_to_hex(sha3(data, b, c, d, r, rounds)))