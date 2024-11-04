#!/usr/bin/env python3

# Importa la libreria di pwntools
from pwn import *


def main():
    HOST = "software-17.challs.olicyber.it"
    PORT = 13000
    r = remote(HOST, PORT)

    #titolo:
    r.recvuntil(b"...")
    r.recvuntil(b"...")
    r.sendline(b"c")#mando il segnale che si può iniziare
    for i in range(10):
        r.recvline()
        somma = r.recvline().decode()
        somma = somma[1:-2].split(", ")
        risposta1 = 0
        for i in somma:
            risposta1 += int(i)
        r.sendline(str(risposta1).encode())
        print(r.recvline())
    print(r.recvline())
    r.close()

'''
    # .send() può essere invocato sull'oggetto ritornato da remote() per inviare dati
    r.send(b"Ciao!")

    # .sendline() è identico a .send(), però appende un newline dopo i dati
    r.sendline(b"Ciao!")

    # .sendafter() e .sendlineafter() inviano la stringa "Ciao!"
    r.sendafter(b"something", b"Ciao!")

    # solo dopo che viene ricevuta la stringa "something"
    r.sendlineafter(b"something", b"Ciao!")

    # .recv() riceve e ritorna al massimo 1024 bytes dalla socket
    data = r.recv(1024)

    # .recvline() legge dalla socket fino ad un newline
    data = r.recvline()

    # .recvuntil() legge dalla socket finchè non viene incontrata la stringa "something"
    data = r.recvuntil(b"something")
'''

if __name__ == "__main__":
    main()
