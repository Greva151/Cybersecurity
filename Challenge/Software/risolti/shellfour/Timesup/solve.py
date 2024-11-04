from z3 import *
from pwn import *

a = BitVec('a', 32)
b = BitVec('b', 32)
c = BitVec('c', 32)

solver = Solver()

equazione = (a + b + c << (((0xff & (a % b))) & 0x1f)) / (0xffffffff & ((2 << ((0xff & a) & 0x1f) ^ 3) * c)) == 0xa4c570
             
solver.add(equazione)

# Verifica se ci sono soluzioni
if solver.check() == sat:
    # Trova la prima soluzione
    model = solver.model()
    
    # Aggiungi un vincolo per evitare di trovare la stessa soluzione
    solver.add(Or(a != model[a], b != model[b], c != model[c]))
    
    # Verifica se ci sono altre soluzioni
    if solver.check() == sat:
        model = solver.model()
        
        a_value = format(model[a].as_long(), 'x')
        b_value = format(model[b].as_long(), 'x')
        c_value = format(model[c].as_long(), 'x')

        with remote("timesup.challs.havce.it", 31338) as r:
            r.recvuntil(b">>> ")
            r.sendline(bytes(a_value.encode()) + b" " + bytes(b_value.encode()) + b" " + bytes(c_value.encode()))
            r.interactive()
