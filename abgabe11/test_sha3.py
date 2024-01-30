import unittest
from unittest.mock import patch
from sha3 import *
from sha3 import _bin_to_hex, _hex_to_bin
import hashlib


class SHA3TestCase(unittest.TestCase):

    #funktioniert zwar noch nicht, aber schon für nächste abgabe
    def test_sha3(self):
        data = ""
        with open("abgabe11/input.txt", "r") as file:
            data = file.read()
        rounds = 24
        d = 224
        r = 1152
        c = 448
        b = c+r
        self.assertEqual(_bin_to_hex(sha3( _hex_to_bin(data), b, c, d, r, rounds)), hashlib.sha3_224(data.encode()).hexdigest())

if __name__ == '__main__':
    unittest.main()