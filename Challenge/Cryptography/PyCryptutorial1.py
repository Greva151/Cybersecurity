from pwn import *
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20

#testo 1
plaintext = 'La lunghezza di questa frase non è divisibile per 8'
key = bytes.fromhex('64c9c80390c012f3')
cipher = DES.new(key, DES.MODE_CBC)
padded = pad(plaintext.encode(), 8, 'x923')
cifrato = cipher.encrypt(padded)
print("1 testo cifrato = " + str(cifrato.hex()))
iv = cipher.iv
print("1 iv = ", iv.hex())

#testo 2
plaintext = "Mi chiedo cosa significhi il numero nel nome di questo algoritmo."
key = get_random_bytes(32)
print("2 chiave = "+ key.hex())
cipher = AES.new(key, AES.MODE_CFB, segment_size = 24)
padded = pad(plaintext.encode(), 16, "pkcs7")
cifrato = cipher.encrypt(padded)
print("2 testo cifrato = ", cifrato.hex())
iv = cipher.iv
print("2 iv = ", iv.hex())

#testo 3
key = bytes.fromhex('c503f32cfcc9ab482fb537db2afdda3525638c66ac8e3bc7fbf83e295ed475c8')
ciphertext = bytes.fromhex("24ad84861211cb5779720b91ca0ecd23d27239d58a6237af5c9b3bac")
iv = bytes.fromhex('96da2471e52cb0e7')
cipher = ChaCha20.new(key = key, nonce = iv)
cifrato = cipher.decrypt(ciphertext)
print(cifrato.decode())