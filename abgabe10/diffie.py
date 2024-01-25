import sys
import random

iList = [1,7,11,13,17,19,23,29]
# n decompse like this: n = 2^k * m
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

# Function to check if a number is prime
def isPrime(n, rounds):
    for _ in range(rounds):
        if not millerRabin(n):
            return False
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
          
# generates p with p = 2q + 1; p and q prime
def generateP(length):
    while True:
        q = generatePrime(length - 1)
        p = 2*q + 1
        if isPrime(p, 100):
            return p

# generates a generator g for p
def getGenerator(p):
    while True:
        h = random.randint(2, p - 1)
        g = pow(h, 2, p)
        if g != 1:
            return g

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: python3 diffie.py <keylength>") # output_file for testing
        exit(1)

    keylength = int(sys.argv[1])

    p = generateP(keylength)
    g = getGenerator(p)

    a = random.randint(2, p-1)
    b = random.randint(2, p-1)

    # calculate secret
    A = pow(g, a, p)
    B = pow(g, b, p)

    # key exchange would happen here
    S = pow(B, a, p)

    print(p)
    print(g)
    print(A)
    print(B)
    print(S)