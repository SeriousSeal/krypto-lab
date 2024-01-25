from  unittest import TestCase
from abgabe1.automatic_decrypt import decrypt, crack_additive_cipher

class TestAutomaticDecrypt(TestCase):
    def test_decrypt(self):
        # Test case 1: key = 3
        data = "VWDPLQD"
        key = 3
        expected_result = "STAMINA"
        self.assertEqual(decrypt(data, key), expected_result)


    def test_crack_additive_cipher(self):
        # Test case 1
        data= ""
        expected_result = ""
        with open("abgabe1/sampleEncrypted.txt", 'r') as plaintext:
            data = plaintext.read()
        
        with open("abgabe1/sampleEncrypted2.txt", 'r') as plaintext:
            expected_result = plaintext.read()
            
        self.assertEqual(crack_additive_cipher(data), expected_result)

