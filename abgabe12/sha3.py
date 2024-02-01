import sys
import re

rotations = [
    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14
]

round_constants = [
    "0000000000000001",
    "0000000000008082",
    "800000000000808A",
    "8000000080008000",
    "000000000000808B",
    "0000000080000001",
    "8000000080008081",
    "8000000000008009",
    "000000000000008A",
    "0000000000000088",
    "0000000080008009",
    "000000008000000A",
    "000000008000808B",
    "800000000000008B",
    "8000000000008089",
    "8000000000008003",
    "8000000000008002",
    "8000000000000080",
    "000000000000800A",
    "800000008000000A",
    "8000000080008081",
    "8000000000008080",
    "0000000080000001",
    "8000000080008008"
]

# xor function for arbitrary number of bit strings
def _xor(*args):
    return ''.join(str(sum(int(b) for b in bits) % 2) for bits in zip(*args))

def _not (a):
    return ''.join('1' if a[i] == '0' else '0' for i in range(len(a)))

def _and(a, b):
    return ''.join('1' if a[i] == '1' and b[i] == '1' else '0' for i in range(len(a)))

# calculate coordinates in a strided string array
# offset of i + offset of j + offset of k
def _calculate_coordinates(i, j, k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + k 

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
    
def rho(A):
    out = ""
    for i in range(25):
        block = A[i*64:(i+1)*64]
        block = block[rotations[i]:] + block[:rotations[i]]
        out += block
    return out


def pi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            out += A[_calculate_coordinates(i, 3*i + j, 0):_calculate_coordinates(i, 3*i + j, 64)]
    return out

def chi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            block = A[_calculate_coordinates(i, j, 0):_calculate_coordinates(i, j, 64)]
            block1 = A[_calculate_coordinates(i, j+1, 0):_calculate_coordinates(i, j+1, 64)]
            block2 = A[_calculate_coordinates(i, j+2, 0):_calculate_coordinates(i, j+2, 64)]
            out += _xor(block, _and(_not(block1), block2))
    return out


def iota(A, i):
    return _xor(A[:64], _hex_to_bin(round_constants[i]))+A[64:]



def f(A, rounds):
    for x in range(rounds):
        A = theta(A)
        A = rho(A)
        A = pi(A)
        A = chi(A)
        A = iota(A,x)    
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
    print(theta("0"*b))
    with open(input_file, "r") as file:
        data = _hex_to_bin(file.read())

    with open(output_file, "w") as file:
        file.write(_bin_to_hex(sha3(data, b, c, d, r, rounds)))