from Crypto.Util.number import getPrime
import io
from scapy.all import *
import random

def get_random_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def get_random_url():
    return ''.join([random.choice([chr(i+ord('a')) for i in range(26)]) for _ in range(8)])

def generate_rsa(CODE):
    check = False
    while not check:
        p = getPrime(64)
        q = getPrime(64)
        n = p*q
        e = 65537
        plaintext = int(CODE)
        ciphertext = pow(plaintext, e, n)
        if len(str(n)) == 39 and len(str(ciphertext)) == 38:
            check = True
    return n, e, ciphertext

def check_query(query):
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "UNION", "EXEC", "CONCAT", "WHEN", "CASE"]
    for keyword in forbidden_keywords:
        if keyword in query.upper():
            return False
    
    if "SELECT" not in query.upper():
        return False

    if ";" in query:
        return False
    
    return True

def create_pcap(n, e, ciphertext):
    pcap = rdpcap("access_log.pcap")
    for el in pcap:
        if Raw in el:
            if el[Raw].load == b'Protocol: RSA\n n:777777777777777777777777777777777777777\ne: 65537':
                el[TCP].payload = Raw(load='Protocol: RSA\n n:{}\ne: {}'.format(n, e).encode())
                del el[IP].chksum  # Recalculate checksum (remove old checksum)
                del el[TCP].chksum # Recalculate TCP checksum
            if el[Raw].load == b'Ciphertext: 88888888888888888888888888888888888888':
                el[TCP].payload = Raw(load='Ciphertext: {}'.format(ciphertext).encode())
                del el[IP].chksum  # Recalculate checksum (remove old checksum)
                del el[TCP].chksum # Recalculate TCP checksum    

    pcap_io = io.BytesIO()
    writer = PcapWriter(pcap_io, sync=True)  # `sync=True` flushes data after each write
    for packet in pcap:
        writer.write(packet)  # Write each packet to the buffer
    pcap_io.seek(0)

    file = io.BytesIO(pcap_io.read())

    return file