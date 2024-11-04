import pyshark
from rich.progress import track

capture = pyshark.FileCapture("capture.pcapng")

stringa = bytes([])

for packet in track(capture, description = "leggendo i byte"):
    if "dns" in packet:
        nome = packet.dns.resp_name
        if len("".join(nome)) == 66:
            try:
                flag = nome[5:53]
                stringa += bytes.fromhex(flag)
            except:
                continue

#stringa = bytes.fromhex(stringa).decode()

with open("foto.zip", "wb") as file:
    file.write(stringa)