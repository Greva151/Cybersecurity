from pwn import *
from rich.progress import track


r = remote("2048.challs.olicyber.it", 10007)
r.recvlines(2)

for i in track(range(2048), description="sto esegunedo i calcoli"):
#for i in range(2048):
    input = [r.recvuntil(b" ").strip().decode(), r.recvuntil(b" ").strip().decode(), r.recvuntil(b" ").strip().decode()]
    #print(i)
    input[1] = int(input[1])
    input[2] = int(input[2])
    risultato = 0
    if input[0] == "SOMMA":
        risultato = input[1] + input[2]
    elif input[0] == "POTENZA":
        risultato = input[1] ** input[2]
    elif input[0] == "DIFFERENZA":
        risultato = input[1] - input[2]
    elif input[0] == "DIVISIONE_INTERA":
        risultato = input[1] // input[2]   
    elif input[0] == "PRODOTTO":
        risultato = input[1] * input[2]
    risultato = str(risultato).encode()
    r.sendline(risultato)

r.interactive()
r.close()
