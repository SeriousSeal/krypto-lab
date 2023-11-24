import sys
from aes import modeECB, modeCBC, modeOFB, modeCTR, read_file_remove_spaces_newlines, write_multiple_matrices_into_file

if len(sys.argv) != 6 and len(sys.argv) != 5:
    print("Usage: python3 aes_encrypt.py <modus> <input_file> <key_file> <output_file> ?<iv_file>")
    sys.exit(1)
modeClass = None
mode = sys.argv[1]
input_file = sys.argv[2]
key_file_name = sys.argv[3]
output_file_name = sys.argv[4]
iv_file_name = sys.argv[5] if len(sys.argv) == 6 else None
if mode != 'ecb' and iv_file_name is  None:
   raise ValueError("Invalid mode. Expected iv file for this mode")

input = read_file_remove_spaces_newlines(input_file)
iv = read_file_remove_spaces_newlines(iv_file_name) if iv_file_name is not None else None

if mode == "ecb":
    modeClass = modeECB(key_file_name)
elif mode == "cbc":
    modeClass = modeCBC(iv, key_file_name)
elif mode == "ofb":
    modeClass = modeOFB(iv, key_file_name)
elif mode == "ctr":
    modeClass = modeCTR(iv, "00000000000000000000000000000000", key_file_name)
else:
    print("Mode not supported")
    sys.exit(1)

cipherMatrix = modeClass.encrypt(input, 128)
write_multiple_matrices_into_file(cipherMatrix, output_file_name)