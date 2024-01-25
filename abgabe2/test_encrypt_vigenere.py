import unittest
from encrypt_vigenere import encrypt

class TestEncrypt(unittest.TestCase):
    def test_encrypt(self):
        # Test case 1: Encrypting uppercase letters with a key
        text = "HELLO"
        key = "KEY"
        expected_output = "RIJVS"
        self.assertEqual(encrypt(text, key), expected_output)


if __name__ == '__main__':
    unittest.main()