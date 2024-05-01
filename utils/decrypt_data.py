import os
import json
from .decrypt import AESdec, DES3dec, BFishdec
from stegano import lsb
import boto3

def decrypt_file(file_to_decrypt,keys_file_url):
    # Generate decrypted file path
    base_name = os.path.basename(file_to_decrypt)
    name, ext = os.path.splitext(base_name)
    decrypted_file_path = os.path.join(os.path.dirname(file_to_decrypt), f"{name}_decrypted{ext}")


    def decrypt_img(bucket_name, object_name):
        # Create a client
        s3 = boto3.client('s3',
                          aws_access_key_id='AKIAXEBZG4JCX67N62PV',
                          aws_secret_access_key='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',
                          region_name='us-east-1')

        # Download the image from the S3 bucket
        try:
            s3.download_file(bucket_name, object_name, 'downloaded_image.png')
        except Exception as e:
            print(f"Error downloading file from S3: {str(e)}")
            return

        # Extract the hidden data from the image
        try:
            secret = lsb.reveal('downloaded_image.png')
        except Exception as e:
            print(f"Error revealing secret from image: {str(e)}")
            return

        return secret
    k=decrypt_img('cryptoproject1', 'intial')
    try:
        # Load the keys and IVs from a file
        with open(keys_file_url, 'r',encoding='utf-8') as f:
            keys = json.load(f)
    except FileNotFoundError:
        print(f"{keys_file_url} file not found.")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {keys_file_url}.")
        return

    aes_key = keys.get('aes', {}).get('key')
    aes_iv = keys.get('aes', {}).get('iv')

    des3_key = keys.get('des3', {}).get('key')
    des3_iv = keys.get('des3', {}).get('iv')

    bfish_key = keys.get('bfish', {}).get('key')
    bfish_iv = keys.get('bfish', {}).get('iv')
    if not all([aes_key, aes_iv, des3_key, des3_iv, bfish_key, bfish_iv]):
        print("One or more keys/IVs are missing from keys.json.")
        return
    # Load the encrypted data from a file
    try:
        with open(file_to_decrypt, 'rb') as file:
            encrypted_data = file.read()
    except FileNotFoundError:
        print(f"{file_to_decrypt} file not found.")
        return

    # Decrypt the data using Blowfish, then 3DES, then AES
    decryption_methods = [BFishdec(bfish_key, bfish_iv), DES3dec(des3_key, des3_iv), AESdec(aes_key, aes_iv)]
    decrypted_data = encrypted_data
    for method in decryption_methods:
        try:
            decrypted_data = method.decrypt(decrypted_data)
            if decrypted_data is None:
                print(f"Decryption failed: {method}")
                return
        except Exception as e:
            print(f"Error decrypting data: {str(e)}")
            return
    # Write the decrypted data to a new file
    try:
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)
    except IOError:
        print(f"Error writing to {decrypted_file_path}.")
        return

    return decrypted_file_path



