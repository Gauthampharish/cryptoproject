# Python
import json
from encrypt import AESenc, DES3enc, BFishenc
from stegano import lsb
from createkey import create_keys  # Import the create_keys function

# Generate and save the keys
keys = create_keys()

aes_key = keys.get('aes', {}).get('key')
aes_iv = keys.get('aes', {}).get('iv')

des3_key = keys.get('des3', {}).get('key')
des3_iv = keys.get('des3', {}).get('iv')

bfish_key = keys.get('bfish', {}).get('key')
bfish_iv = keys.get('bfish', {}).get('iv')

if not all([aes_key, aes_iv, des3_key, des3_iv, bfish_key, bfish_iv]):
    print("One or more keys/IVs are missing from keys.json.")
    exit(1)

# Get the file to be encrypted
try:
    with open('hello.txt', 'rb') as file:
        data = file.read()
except FileNotFoundError:
    print("file_to_encrypt.txt file not found.")
    exit(1)

# Encrypt the file data using AES, then 3DES, then Blowfish
encryption_methods = [AESenc(aes_key, aes_iv), DES3enc(des3_key, des3_iv), BFishenc(bfish_key, bfish_iv)]
encrypted_data = data
for method in encryption_methods:
    try:
        encrypted_data = method.encrypt(encrypted_data)
    except Exception as e:
        print(f"Error encrypting data: {str(e)}")
        exit(1)

# Save the encrypted data to an image
try:
    with open('encrypted_data.bin', 'wb') as file:
        file.write(encrypted_data)
except IOError:
    print("Error writing to encrypted_data.bin.")
    exit(1)