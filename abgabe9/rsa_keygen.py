import sys
import random

iList = [1,7,11,13,17,19,23,29]

def phi(prime1, prime2):
    return (prime1 - 1) * (prime2 - 1)

def decomposeToPowerOfTwo(n):
    k, m = 0, n
    while m % 2 == 0:
        k += 1
        m //= 2
    return k, m

#Implemented millerRabin
def millerRabin(n):
    k, m = decomposeToPowerOfTwo(n-1)
    a = random.randint(2, n-1)
    b = pow(a, m, n)
    if b % n == 1:
        return True
    for _ in range(k):
        if b % n == n-1:
            return True
        b = pow(b, 2, n)
    return False

#Implemented expandedEuclid
def expandedEuclid(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

# Function to check if a number is prime
def isPrime(n, rounds):
    # Perform the Miller-Rabin test for the specified number of rounds
    for _ in range(rounds):
        if not millerRabin(n):
            return False
    # If n passes all rounds of the test, it is probably prime
    return True

# Function to generate a prime number of the given length
def generatePrime(length):
    prime_candidate_base = random.randint(2**(length-1), 2**length-1)
    prime_remainder_index = 0
    while True:
        prime_candidate = 30 * prime_candidate_base + iList[prime_remainder_index % len(iList)]
        if isPrime(prime_candidate, 100):
            return prime_candidate
        prime_remainder_index += 1
        if prime_remainder_index % len(iList) == 0:
            prime_candidate_base += 1

if (len(sys.argv) != 5):
    print("Usage: python3 rsa_keygen.py <length> <output_private_key> <output_public_key> <output_primes>")
    exit(1)
    
length = int(sys.argv[1])
output_private_key = sys.argv[2]
output_public_key = sys.argv[3]
output_primes = sys.argv[4]

p = generatePrime(length)
q = generatePrime(length)

e = 2**16 + 1 
phi_P_Q = phi(p, q)

while (expandedEuclid(e, phi_P_Q)[0] != 1):
    e = random.randint(2, phi_P_Q-1)    
d = expandedEuclid(e, phi_P_Q)[1] % phi_P_Q

with open(output_private_key, "w") as f:
    f.write(str(d) + "\n" + str(phi_P_Q))
    
with open(output_public_key, "w") as f:
    f.write(str(e) + "\n" + str(phi_P_Q))
    
with open(output_primes, "w") as f:
    f.write(str(p) + "\n" + str(q))