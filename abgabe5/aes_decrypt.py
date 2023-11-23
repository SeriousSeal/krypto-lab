import sys
import aes_encrypt

if len(sys.argv) != 6 and len(sys.argv) != 5:
    print("Usage: python3 aes.py <modus> <input_file> <key_file> <output_file> ?<iv_file>")
    sys.exit(1)

mode = sys.argv[1].
input_file = sys.argv[2]
key_file_name = sys.argv[3]
output_file_name = sys.argv[4]
iv_file_name = sys.argv[5] if len(sys.argv) == 6 else None
if mode != 'ecb' and iv_file_name is  None:
   raise ValueError("Invalid mode. Expected iv file for this mode")

result_matrix = aes_encrypt.AES_Cipher('encrypt', aes_encrypt.read_matrixfile_into_matrix(input_file), aes_encrypt.read_file_into_matrix(key_file_name))
aes_encrypt.write_matrix_into_file(result_matrix, output_file_name)