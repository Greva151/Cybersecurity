from pwn import *
from string import printable

r = remote("benchmark.challs.cyberchallenge.it", 9031)

flag = "CCIT{s1d3_ch4nn3ls_r_c00l}"

while 1:
    
    nuovalettera = ""
    punteggioScorso = 0
    
    for carattere in range(37, 127):
        r.recvuntil(b"check:")
        lettera = chr(carattere)
        r.sendline((flag + lettera).encode())
        punteggio = int(r.recvuntil(b"cycles").decode().split()[4])
        if(punteggioScorso < punteggio):
            punteggioScorso = punteggio
            nuovalettera = lettera
    
    flag += nuovalettera
            

r.interactive()