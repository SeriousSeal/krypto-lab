import unittest
from rsa_keygen import *

class RSAKeygenTestCase(unittest.TestCase):
    def test_keygen(self):
        length = 100
        p = generatePrime(length)
        q = generatePrime(length)

        (e, n), (d, n) = genRSAKeys(p,q)
        self.assertEqual((d*e)%((p-1)*(q-1)),1)
        self.assertEqual(n, p*q)

if __name__ == '__main__':
    unittest.main()