import unittest
from unittest.mock import patch
from aes_decrypt import modeECB, modeCBC, modeOFB, modeCTR, read_file_remove_spaces_newlines, write_multiple_matrices_into_file
from aes_encrypt import modeECB, modeCBC, modeOFB, modeCTR, read_file_remove_spaces_newlines, write_multiple_matrices_into_file

class TestAES(unittest.TestCase):
    def test_modeECB(self):
        input_file = "abgabe5/Beispiel_1_Klartext.txt"
        key_file = "abgabe5/Beispiel_key.txt"
        iv_file = "abgabe5/iv.txt"
        
        input = read_file_remove_spaces_newlines(input_file)
        iv = read_file_remove_spaces_newlines(iv_file) if iv_file is not None else None
        
        mode = modeECB(key_file)
        cipherMatrix = mode.encrypt(input, 128)
        cipherString = ""
        
        for matrix in cipherMatrix:
            for row in matrix:
              cipherString += (" ".join(row).replace("0x", "") + " ")
            cipherString += "\n"
            
        
        mode = modeECB(key_file)
        plainMatrix = mode.decrypt(cipherString.replace(' ', '').replace('\n', ''), 128)
        plainString = ""
        for matrix in plainMatrix:
            for row in matrix:
              plainString += (" ".join(row).replace("0x", "") + " ")
            plainString += "\n"
            
        self.assertEqual(plainString.replace(' ', '').replace('\n', ''), input.strip())
        
        

    
    def test_modeCBC(self):
        input_file = "abgabe5/Beispiel_1_Klartext.txt"
        key_file = "abgabe5/Beispiel_key.txt"
        iv_file = "abgabe5/iv.txt"
        
        input = read_file_remove_spaces_newlines(input_file)
        iv = read_file_remove_spaces_newlines(iv_file) if iv_file is not None else None
        
        mode = modeCBC(iv, key_file)
        cipherMatrix = mode.encrypt(input, 128)
        cipherString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              cipherString += (" ".join(row).replace("0x", "") + " ")
            cipherString += "\n"
        
        mode = modeCBC(iv, key_file)
        cipherMatrix = mode.decrypt(cipherString.replace(' ', '').replace('\n', ''), 128)
        plainString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              plainString += (" ".join(row).replace("0x", "") + " ")
            plainString += "\n"
            
        self.assertEqual(plainString.replace(' ', '').replace('\n', ''), input.strip())
        
    def test_modeOFB_decrypt(self):
        input_file = "abgabe5/Beispiel_1_Klartext.txt"
        key_file = "abgabe5/Beispiel_key.txt"
        iv_file = "abgabe5/iv.txt"
        
        input = read_file_remove_spaces_newlines(input_file)
        iv = read_file_remove_spaces_newlines(iv_file) if iv_file is not None else None
        
        mode = modeOFB(iv, key_file)
        cipherMatrix = mode.encrypt(input, 128)
        cipherString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              cipherString += (" ".join(row).replace("0x", "") + " ")
            cipherString += "\n"
        
        mode = modeOFB(iv, key_file)
        cipherMatrix = mode.decrypt(cipherString.replace(' ', '').replace('\n', ''), 128)
        plainString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              plainString += (" ".join(row).replace("0x", "") + " ")
            plainString += "\n"
            
        self.assertEqual(plainString.replace(' ', '').replace('\n', ''), input.strip())
        
    def test_modeCTR_decrypt(self):
        input_file = "abgabe5/Beispiel_1_Klartext.txt"
        key_file = "abgabe5/Beispiel_key.txt"
        iv_file = "abgabe5/iv.txt"
        counter = "00000000000000000000000000000000"
        
        input = read_file_remove_spaces_newlines(input_file)
        iv = read_file_remove_spaces_newlines(iv_file) if iv_file is not None else None
        
        mode = modeCTR(iv, counter, key_file)
        cipherMatrix = mode.encrypt(input, 128)
        cipherString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              cipherString += (" ".join(row).replace("0x", "") + " ")
            cipherString += "\n"
        
        mode = modeCTR(iv, counter, key_file)
        cipherMatrix = mode.decrypt(cipherString.replace(' ', '').replace('\n', ''), 128)
        plainString = ""
        for matrix in cipherMatrix:
            for row in matrix:
              plainString += (" ".join(row).replace("0x", "") + " ")
            plainString += "\n"
            
        self.assertEqual(plainString.replace(' ', '').replace('\n', ''), input.strip())

if __name__ == '__main__':
    unittest.main()