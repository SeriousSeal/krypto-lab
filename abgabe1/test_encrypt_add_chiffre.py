from  unittest import TestCase
from abgabe1.encrypt_add_chiffre import encrypt

class TestEncryptAddChiffre(TestCase):
    def test_encrypt(self):
        # Test case 1: key = 3
        data = "HELLO"
        key = 3
        expected_result = "KHOOR"
        self.assertEqual(encrypt(data, key), expected_result)

