# Python
from Crypto.Cipher import AES, DES3, Blowfish
from Crypto.Util.Padding import unpad
from stegano import lsb
import json

class AESdec:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def decrypt(self, ciphertext):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            return unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
        except ValueError:
            print("Incorrect decryption")

class DES3dec:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def decrypt(self, ciphertext):
        try:
            cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
            return unpad(cipher.decrypt(ciphertext[DES3.block_size:]), DES3.block_size)
        except ValueError:
            print("Incorrect decryption")

class BFishdec:
    def __init__(self, key, iv):
        self.key = bytes.fromhex(key)  # Convert hex string to bytes
        self.iv = bytes.fromhex(iv)

    def decrypt(self, ciphertext):
        try:
            print(f"Key: {self.key}")
            print(f"IV: {self.iv}")
            print(f"Ciphertext: {ciphertext}")
            cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
            return unpad(cipher.decrypt(ciphertext[Blowfish.block_size:]), Blowfish.block_size)
        except ValueError:
            print("Incorrect decryption")
class ImageSteg:
    def __init__(self, image_path):
        self.image_path = image_path

    def reveal_data(self):
        try:
            return lsb.reveal(self.image_path)
        except Exception as e:
            print(f"Error revealing data: {str(e)}")