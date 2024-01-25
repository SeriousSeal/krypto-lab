import unittest
from unittest.mock import patch
from diffie import *

class DiffieTestCase(unittest.TestCase):

    def test_getGenerator(self):
        p = generateP(100)
        g = getGenerator(p)
        self.assertNotEqual(g, 1)
        self.assertNotEqual(g, p - 1)
        self.assertEqual(pow(g, (p - 1) // 2, p), 1)
        
    def test_secret(self):
        p = generateP(100)
        g = getGenerator(p)
        a = random.randint(2, p-1)
        b = random.randint(2, p-1)
        B = pow(g, b, p)
        S = pow(B, a, p)
        self.assertEqual(pow(g, a*b, p), S)


if __name__ == '__main__':
    unittest.main()