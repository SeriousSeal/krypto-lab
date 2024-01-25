import unittest
from spn import spn, _binary_to_hex

class SPNTestCase(unittest.TestCase):
    def test_spn(self):
        # Test case 1
        input1 = '0123'
        key1 = 'abcd'
        expected_output1 = '4bc6'
        self.assertEqual(_binary_to_hex(spn(input1, key1)), expected_output1)


if __name__ == '__main__':
    unittest.main()