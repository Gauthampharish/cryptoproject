from Crypto.Cipher import AES, DES3, Blowfish
from Crypto.Random import get_random_bytes
import json

def create_keys():
    # Generate keys and IVs
    aes_key = get_random_bytes(16).hex()
    aes_iv = get_random_bytes(AES.block_size).hex()

    des3_key = get_random_bytes(24).hex()
    des3_iv = get_random_bytes(DES3.block_size).hex()

    bfish_key = get_random_bytes(56).hex()
    bfish_iv = get_random_bytes(Blowfish.block_size).hex()

    # Save the keys and IVs to a file
    keys = {
        'aes': {
            'key': aes_key,
            'iv': aes_iv
        },
        'des3': {
            'key': des3_key,
            'iv': des3_iv
        },
        'bfish': {
            'key': bfish_key,
            'iv': bfish_iv
        }
    }

    with open('keys.json', 'w') as f:
        json.dump(keys, f)

    return keys