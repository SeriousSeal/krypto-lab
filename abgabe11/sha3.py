import sys
import re

rotations =  [[0, 1, 62, 28, 27],
            [36, 44, 6, 55, 20],
            [3, 10, 43, 25, 39],
            [41, 45, 15, 21, 8],
            [18, 2, 61, 56, 14]]

round_constants_String = [
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

# not function for arbitrary number of bit strings
def _not (a):
    return ''.join('1' if a[i] == '0' else '0' for i in range(len(a)))

# and function for arbitrary number of bit strings
def _and(a, b):
    return ''.join('1' if a[i] == '1' and b[i] == '1' else '0' for i in range(len(a)))

# calculate coordinates in a strided string array
# offset of i + offset of j + offset of k
def _calculate_coordinates(i, j, k):
    return (i % 5) * 5 * 64 + (j % 5) * 64 + (k % 64)

# converts 8 bit binary to 2 hex
def _convert_8BitTo2Hex(binary):
    return hex(int(binary[::-1], 2))[2:].zfill(2)

# converts 2 hex to 8 bit binary
def _bin_to_hex(binary):
    return "".join([_convert_8BitTo2Hex(binary[i:i+8]) for i in range(0, len(binary), 8)])

# removes non hex characters from string
def clean_Hex(hex):
    return re.sub(r"[^A-Fa-f0-9]", '', hex).lower()

# converts 2 hex to 8 bit binary
def _convert_2HexTo8Bit(hex):
    return bin(int(hex, 16))[2:].zfill(8)[::-1]

# converts hex string to bin string
def _hex_to_bin(hex):
    hex = clean_Hex(hex)
    return "".join([_convert_2HexTo8Bit(hex[i:i+2]) for i in range(0, len(hex), 2)])

# calculates parity
def _parity(A, j, k, dimension_size):
    column_indices = [_calculate_coordinates(i, j, k) for i in range(dimension_size)]
    return _xor(*[A[idx] for idx in column_indices])

# pads the input string
def _pad(N, r):
    N += "1"
    padded = []
    while len(N) % (r-1) != 0:
        N += "0"
    N += "1"
    for i in range(0, len(N), r):
        padded.append(N[i:i+r])
    return padded

round_constants_String = ["".join((hex[14:16],hex[12:14],hex[10:12],hex[8:10],hex[6:8],hex[4:6],hex[2:4],hex[0:2])) for hex in round_constants_String]
round_constants = [_hex_to_bin(hex) for hex in round_constants_String]

# implement theta
def theta(A):
    out = []
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out.append(_xor(A[_calculate_coordinates(i,j,k)], _parity(A,j-1,k,5),_parity(A,j+1,k-1,5)))
    return ''.join(out)

# implement rho
def rho(A):
    out = ""
    for i in range(5):
        for j in range(5):
            block = A[_calculate_coordinates(i,j,0):_calculate_coordinates(i,j,0)+64]
            out += block[64-rotations[i][j]:]+block[:64-rotations[i][j]]
    return out

# implement pi
def pi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            
            out += A[_calculate_coordinates(j,3*i + j,0):_calculate_coordinates(j,3*i + j,0)+64]
    return out

# implement chi
def chi(A):
    out = ""
    for i in range(5):
        for j in range(5):
            block = A[_calculate_coordinates(i, j, 0):_calculate_coordinates(i, j, 0)+64]
            block1 = A[_calculate_coordinates(i, j+1, 0):_calculate_coordinates(i, j+1, 0)+64]
            block2 = A[_calculate_coordinates(i, j+2, 0):_calculate_coordinates(i, j+2, 0)+64]
            out += _xor(block, _and(_not(block1), block2))
    return out

# implement iota
def iota(A, i):
    return _xor(A[:64],round_constants[i])+A[64:]

# implement f
def f(A, rounds):
    for x in range(rounds):
        A = theta(A)
        A = rho(A)
        A = pi(A)
        A = chi(A)
        A = iota(A,x) 
    return A

# implement sha3
def sha3(str, b, c, d, r, rounds):
    str = str + "01"
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