# Python
import json
from decrypt import AESdec, DES3dec, BFishdec

try:
    # Load the keys and IVs from a file
    with open('keys.json', 'r') as f:
        keys = json.load(f)
except FileNotFoundError:
    print("keys.json file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error decoding JSON from keys.json.")
    exit(1)

aes_key = keys.get('aes', {}).get('key')
aes_iv = keys.get('aes', {}).get('iv')

des3_key = keys.get('des3', {}).get('key')
des3_iv = keys.get('des3', {}).get('iv')

bfish_key = keys.get('bfish', {}).get('key')
bfish_iv = keys.get('bfish', {}).get('iv')

if not all([aes_key, aes_iv, des3_key, des3_iv, bfish_key, bfish_iv]):
    print("One or more keys/IVs are missing from keys.json.")
    exit(1)

# Load the encrypted data from a file
try:
    with open('encrypted_data.bin', 'rb') as file:
        encrypted_data = file.read()
except FileNotFoundError:
    print("encrypted_data.bin file not found.")
    exit(1)

# Decrypt the data using Blowfish, then 3DES, then AES
decryption_methods = [BFishdec(bfish_key, bfish_iv), DES3dec(des3_key, des3_iv), AESdec(aes_key, aes_iv)]
decrypted_data = encrypted_data
for method in decryption_methods:
    try:
        decrypted_data = method.decrypt(decrypted_data)
        if decrypted_data is None:
            print("Decryption failed.", method)
            exit(1)
    except Exception as e:
        print(f"Error decrypting data: {str(e)}")
        exit(1)

# Write the final decrypted data to a file
try:
    with open('decrypted_file.txt', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
except IOError:
    print("Error writing to decrypted_file.txt.")
    exit(1)