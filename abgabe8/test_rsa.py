import unittest
from rsa import rsa

class RSATestCase(unittest.TestCase):

    def test_rsa_encrypt(self):        

        key, e, n, message = "", 0, 0, ""

        with open("abgabe8/ExampleKey.txt", "r") as f:
            key = f.read().splitlines()
            e = int(key[0])
            n = int(key[1])

        with open("abgabe8/ExampleText.txt", "r") as f:
            message = f.read().splitlines()
            message = int(message[0])
            
        with open("abgabe8/ExampleEncrypted.txt", "r") as f:
            expected = f.read()

        encrypted = rsa(message, e, n)
        self.assertEqual(encrypted, int(expected))
        
    def test_rsa_decrypt(self):        

        key, e, n, message = "", 0, 0, ""

        with open("abgabe8/ExampleKeyDecrypt.txt", "r") as f:
            key = f.read().splitlines()
            e = int(key[0])
            n = int(key[1])

        with open("abgabe8/ExampleEncrypted.txt", "r") as f:
            message = f.read().splitlines()
            message = int(message[0])
            
        with open("abgabe8/ExampleText.txt", "r") as f:
            expected = f.read()

        encrypted = rsa(message, e, n)
        self.assertEqual(encrypted, int(expected))

        

if __name__ == '__main__':
    unittest.main()