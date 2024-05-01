# Python
from Crypto.Cipher import AES, DES3, Blowfish
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from stegano import lsb
import json

class AESenc:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def encrypt(self, message):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            return self.iv + cipher.encrypt(pad(message, AES.block_size))
        except Exception as e:
            print(f"Error encrypting with AES: {str(e)}")
            return None

class DES3enc:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def encrypt(self, message):
        try:
            cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
            return self.iv + cipher.encrypt(pad(message, DES3.block_size))
        except Exception as e:
            print(f"Error encrypting with DES3: {str(e)}")
            return None

class BFishenc:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def encrypt(self, message):
        try:
            cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
            return self.iv + cipher.encrypt(pad(message, Blowfish.block_size))
        except Exception as e:
            print(f"Error encrypting with Blowfish: {str(e)}")
            return None
