import time

from scapy.contrib.automotive.uds import UDS, UDS_NR
from scapy.packet import Raw


import config
import global_stuff as gl
from classes import SA_seed


def send_msg(pkt):
    print(f"The server sent: {bytes(pkt).hex()}\n\n{pkt.show2(dump=True)}\n", flush=True)
    return


def security_access(pkt):
    from scapy.contrib.automotive.uds import UDS_SA, UDS_SAPR
    security_level = pkt[UDS][UDS_SA].securityAccessType

    if gl.SEND_ENOA:
        if time.time() - gl.TIME_ENOA_ACTIVATED > config.SEED_REQUEST_TIMEOUT:
            gl.SEND_ENOA = False
            gl.TIME_ENOA_ACTIVATED = 0
            gl.RETRIES = 0
        else:
            send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x36))
            return

    if gl.CURRENT_SESSION not in config.SECURITY_ACCESS_LEVELS:
        send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x7F))
        return

    if security_level % 2 == 0:
        if security_level - 1 not in config.SECURITY_ACCESS_LEVELS[gl.CURRENT_SESSION]:
            send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x12))
            gl.SEED = None
            return

        if gl.SEED is None:
            send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x24))
            return

        if config.key_check(pkt[UDS][UDS_SA].securityKey, security_level):
            gl.RETRIES = 0
            gl.AUTH = True
            gl.SEED = None
            send_msg(UDS() / UDS_SAPR(securityAccessType=security_level))
        else:
            gl.SEED = None
            gl.RETRIES += 1
            if gl.RETRIES >= config.SEED_REQUEST_RETRIES:
                gl.SEND_ENOA = True
                gl.TIME_ENOA_ACTIVATED = time.time()
            send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x35))
    else:
        if security_level not in config.SECURITY_ACCESS_LEVELS[gl.CURRENT_SESSION]:
            send_msg(UDS() / UDS_NR(requestServiceId=0x27, negativeResponseCode=0x12))
            return
        if gl.SEED is None or not gl.SEED.is_valid() or gl.SEED.level != security_level:
            gl.SEED = SA_seed(security_level)
        send_msg(UDS() / UDS_SAPR(securityAccessType=security_level, securitySeed=gl.SEED.seed))
