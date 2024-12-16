import ctypes
import os

QUEUE_SIZE = 2
SUPPORTED_SERVICES = {0x27}
SECURITY_ACCESS_LEVELS = {1: [1, 2, 3], 2: [1, 3, 9], 3: [1, 3]}
DEFAULT_SESSION = 1
SESSION_RESET_TIMEOUT = 200
BOOTLOADR_SWITCH_TIMEOUT = 0
SEED_REQUEST_TIMEOUT = 7
SEED_REQUEST_RETRIES = 3
IFACE = 'vcan0'
TX_ID = 0x7B0
RX_ID = 0x7D0

lib = ctypes.CDLL('./keygen.so')
lib.fromSeedToKey.argtypes = [ctypes.c_char_p]
lib.fromSeedToKey.restype = ctypes.c_char_p


def key_check(key, access_level):
    from global_stuff import SEED
    result = lib.fromSeedToKey(SEED.seed.hex().encode('utf-8'))
    gen_key = ctypes.string_at(result).decode('utf-8')
    if key.hex() == gen_key and access_level - 1 == SEED.level and SEED.is_valid():
        print(f"Good job! Here's flag: {os.environ['flag']}")
    return key.hex() == gen_key and access_level - 1 == SEED.level and SEED.is_valid()
