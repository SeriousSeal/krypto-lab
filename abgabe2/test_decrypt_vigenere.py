import unittest
from decrypt_vigenere import calculate_coincidence_index, key_length_analysis, determine_key, decrypt

class TestDecryptVigenere(unittest.TestCase):
    plain = ""
    crypto = ""
    
    with open("abgabe2/Klartext_1.txt", 'r') as plaintext:
        plain = plaintext.read()
        
    with open("abgabe2/Kryptotext_TAG.txt", 'r') as plaintext:
        crypto = plaintext.read()


    def test_decrypt(self):
        text = self.crypto
        key = determine_key(self.crypto)
        expected_decrypted_data = self.plain
        self.assertEqual(decrypt(text, key), expected_decrypted_data)

if __name__ == '__main__':
    unittest.main()