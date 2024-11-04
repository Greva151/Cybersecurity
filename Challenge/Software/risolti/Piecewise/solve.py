from pwn import *

def conn():
    r = remote("piecewise.challs.cyberchallenge.it", 9110)

    return r


def main():
    r = conn()
    
    while True:
    
        frase = r.recvline().split()
        
        print(frase)
        
        numero = frase[5]

        if numero.decode("UTF-8") == "line":
            r.sendline("")
        else:
            numero = int(numero)
            
            if frase[8] == b"64-bit":
                if frase[9] == b"big-endian":
                    r.send(numero.to_bytes(8, byteorder="big"))
                else:
                    r.send(numero.to_bytes(8, byteorder="little"))
            else:
                if frase[9] == b"big-endian":
                    r.send(numero.to_bytes(4, byteorder="big"))
                else:
                    r.send(numero.to_bytes(4, byteorder="little"))

        print(r.recvline().split()[2])   


    r.interactive()


if __name__ == "__main__":
    main()