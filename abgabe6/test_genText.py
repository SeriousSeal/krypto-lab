import unittest
from genText import generate_hex_codes

class GenTextTestCase(unittest.TestCase):
    def test_generate_hex_codes(self):
        # Test case 1
        num_times1 = 5
        self.assertEqual(len(generate_hex_codes(num_times1).replace(' ', '').replace('\n', '')), num_times1*4)


if __name__ == '__main__':
    unittest.main()