import unittest
from unittest.mock import patch
from checkQualityLinApprox import *

class CheckQualityLinApproxTestCase(unittest.TestCase):

    def test_main(self):

        sbox = read_file_remove_spaces_newlines("abgabe7/Beispiel_SBox.txt")

        V = [hex_to_bin(sbox[i]) for i in range(16)]
        U = [format(i, '04b') for i in range(16)]

        approximation = read_hex_file('abgabe7/Beispiel_Approximation.txt')
        if any(approximation[i] == '00' for i in [1, 5, 9, 11]):
            print(-1)
            sys.exit(1)

        approximation = [hex_to_bin(approximation[i]) for i in [1, 5, 9, 11]]
        quality = calculateQuality(U, V, approximation)
        self.assertEqual(quality, 0.00390625)

if __name__ == '__main__':
    unittest.main()