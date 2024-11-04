from pwn import *

exe = ELF("./sw-19")

p = remote("software-19.challs.olicyber.it", 13002)

p.recvuntil(b"...")
p.recvuntil(b"...")
p.sendline(b"c")

for i in range(20):
    stringa = p.recvuntil(b": ").decode().split(" ")[1][:-1]
    dizionario = hex(exe.sym[stringa]).encode()
    p.sendline(dizionario)

p.interactive()