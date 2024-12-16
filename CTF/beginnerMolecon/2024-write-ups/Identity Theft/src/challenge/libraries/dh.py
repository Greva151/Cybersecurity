from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import hashlib
import os
from Crypto.Util.number import long_to_bytes, getStrongPrime

NBITS = int(os.getenv("NBITS"))
assert(NBITS)

def get_parameters():
    p = getStrongPrime(NBITS)
    return 2, p

def keygen(g: int, p: int):
    secret = random.randint(1, p)
    return secret, pow(g, secret, p)

def hash(secret):
    return hashlib.sha256(long_to_bytes(secret)).digest()[:16]

def gen_shared_key(pubK: int, privK: int, p: int) -> bytes:
    sk = pow(pubK, privK, p)
    return hash(sk)

def aes_encrypt(key: bytes, msg: str) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(msg.encode(), 16)).hex()

def aes_decrypt(key: bytes, msg_hex: str) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(bytes.fromhex(msg_hex)), 16)

