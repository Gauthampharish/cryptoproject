# Python
import json
from .encrypt import AESenc, DES3enc, BFishenc
from stegano import lsb
from .createkey import create_keys
import os

def encrypt_file(input_file):
    # Generate output file path
    base_name = os.path.basename(input_file)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(os.path.dirname(input_file), f"{name}_encrypted{ext}")

    # Generate keys file path
    keys_file = os.path.join(os.path.dirname(input_file), f"{name}_keys.json")

    keys = create_keys()

    # Save the keys to a file
    with open(keys_file, 'w') as f:
        json.dump(keys, f)

    # Load the keys from the file
    with open(keys_file, 'r') as f:
        keys = json.load(f)

    aes_key = keys.get('aes', {}).get('key')
    aes_iv = keys.get('aes', {}).get('iv')

    des3_key = keys.get('des3', {}).get('key')
    des3_iv = keys.get('des3', {}).get('iv')

    bfish_key = keys.get('bfish', {}).get('key')
    bfish_iv = keys.get('bfish', {}).get('iv')

    if not all([aes_key, aes_iv, des3_key, des3_iv, bfish_key, bfish_iv]):
        raise Exception("One or more keys/IVs are missing from keys.json.")

    try:
        with open(input_file, 'rb') as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"{input_file} file not found.")

    encryption_methods = [AESenc(aes_key, aes_iv), DES3enc(des3_key, des3_iv), BFishenc(bfish_key, bfish_iv)]
    encrypted_data = data
    for method in encryption_methods:
        encrypted_data = method.encrypt(encrypted_data)

    try:
        with open(output_file, 'wb') as file:
            file.write(encrypted_data)
    except IOError:
        raise IOError(f"Error writing to {output_file}.")

    return output_file, keys_file