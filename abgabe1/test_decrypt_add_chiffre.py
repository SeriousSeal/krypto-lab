from  unittest import TestCase
from abgabe1.decrypt_add_chiffre import decrypt

class TestDecryptAddChiffre(TestCase):
    def test_decrypt(self):
        # Test case 1: key = 3
        data = "VWDPLQD"
        key = 3
        expected_result = "STAMINA"
        self.assertEqual(decrypt(data, key), expected_result)
