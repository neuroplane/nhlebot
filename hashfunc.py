import hashlib
import binascii
hex_string = '000000013e2a5b71000003a0'
print(hashlib.md5(binascii.unhexlify(hex_string)).hexdigest())