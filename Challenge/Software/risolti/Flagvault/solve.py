#!/usr/bin/env python3

from pwn import *

exe = ELF("./flagvault_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("flagvault.challs.olicyber.it", 34000)

    return r


def main():
    r = conn()

    r.recvline()

    r.sendline(b"49CMO:N?O2CDI")
    
    r.interactive()


if __name__ == "__main__":
    main()
