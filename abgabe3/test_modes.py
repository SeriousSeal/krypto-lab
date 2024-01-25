import unittest
from modes import modeECB, modeCBC, modeOFB, modeCTR

class TestModes(unittest.TestCase):
    def test_modeECB(self):
        mode = modeECB()
        plaintext = "hello world"
        blocklength = 8
        ciphertext = mode.encrypt(plaintext, blocklength)
        decrypted = mode.decrypt(ciphertext,blocklength)
        self.assertEqual(decrypted, plaintext)

    def test_modeCBC(self):
        mode = modeCBC("00000000")
        plaintext = "hello world"
        blocklength = 8
        ciphertext = mode.encrypt(plaintext, blocklength)
        decrypted = mode.decrypt(ciphertext, blocklength)
        self.assertEqual(decrypted, plaintext)

    def test_modeOFB(self):
        mode = modeOFB("00000000")
        plaintext = "hello world"
        blocklength = 8
        ciphertext = mode.encrypt(plaintext, blocklength)
        decrypted = mode.decrypt(ciphertext, blocklength)
        self.assertEqual(decrypted, plaintext)

    def test_modeCTR(self):
        mode = modeCTR("00000000", "00000000")
        plaintext = "hello world"
        blocklength = 8
        ciphertext = mode.encrypt(plaintext, blocklength)
        decrypted = mode.decrypt(ciphertext, blocklength)
        print(decrypted + "111")
        self.assertEqual(decrypted, plaintext)

if __name__ == '__main__':
    unittest.main()