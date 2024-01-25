import unittest
from aes import AES_Cipher , read_matrixfile_into_matrix, read_file_into_matrix

class TestAESCipher(unittest.TestCase):
    def test_encrypt(self):
        crypto = ""
        with open("abgabe4/Beispiel_1_Kryptotext.txt", 'r') as plaintext:
            crypto = plaintext.read()
        result = AES_Cipher("encrypt", read_matrixfile_into_matrix("abgabe4/Beispiel_1_Klartext.txt"), read_file_into_matrix("abgabe4/Beispiel_key.txt"))
        result_txt=""
        for row in result:
            result_txt += " ".join(row).replace("0x", "") + " "

        self.assertEqual(result_txt.strip(), crypto)

    def test_decrypt(self):
        plaintext = ""
        with open("abgabe4/Beispiel_1_Klartext.txt", 'r') as plaintext:
            plaintext = plaintext.read()
        result = AES_Cipher("decrypt", read_matrixfile_into_matrix("abgabe4/Beispiel_1_Kryptotext.txt"), read_file_into_matrix("abgabe4/Beispiel_key.txt"))
        result_txt=""
        for row in result:
            result_txt += " ".join(row).replace("0x", "") + " "
        self.assertEqual(result_txt.strip(), plaintext)

if __name__ == '__main__':
    unittest.main()