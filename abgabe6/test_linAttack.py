import unittest
from linAttack import *

class LinAttackTestCase(unittest.TestCase):
    @unittest.SkipTest
    def test_linAttack(self):
        input_text = read_file_remove_spaces_newlines("abgabe6/plain.txt")
        input_array = [hex_to_binary(input_text[i:i+4]) for i in range(0, len(input_text), 4)]

        cipher_text = read_file_remove_spaces_newlines("abgabe6/cipher.txt")
        cipher_array = [hex_to_binary(cipher_text[i:i+4]) for i in range(0, len(cipher_text), 4)]

        #plain and cipher text pairs
        M = [(input_array[i], cipher_array[i]) for i in range(len(input_array))]

        maxkey = getMaxKey(M)
        self.assertEqual(binary_to_hex(maxkey[0]+maxkey[1]), "be")
        

        
if __name__ == '__main__':
    unittest.main()