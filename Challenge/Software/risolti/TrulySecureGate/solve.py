#Gregorio Maria Vallé 5^C Informatica 29/10/2023

from pwn import *

exe = ELF("./trulySecureGate_patched")

context.binary = exe

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("tsg.challs.olicyber.it", 14000)

    return r


def main():
    r = conn()

    r.recvuntil(b"NSA-secret-supercomputer-2:/$")

    r.sendline(b"cat flag.txt")
    
    r.recvuntil(b"Password: ")

    r.interactive()
    
    


if __name__ == "__main__":
    main()
