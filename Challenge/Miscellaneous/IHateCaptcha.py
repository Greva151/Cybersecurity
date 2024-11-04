from pwn import *

r = remote("ihc.challs.olicyber.it", 34008)
lettereFlag = ""
print(r.recvuntil("!"))
print(r.recvuntil("!"))
r.send("\n")

for i in range(200):
    input = r.recvline(1).decode().split(" ")
    print(input)

    if input[3] == "risultato":
        if input[5] == "(troncato)":
            r.sendline(str(int(int(input[6]) / int(input[8][:-2]))).encode())
        else:
            input[7] = input[7][:-2]
            if input[6] == "+":
                r.sendline(str(int(input[5]) + int(input[7])).encode())
            if input[6] == "-":
                r.sendline(str(int(input[5]) - int(input[7])).encode())
            if input[6] == '*':
                r.sendline(str(int(input[5]) * int(input[7])).encode())

    elif input[4] == "contrario:":
        input[5] = input[5][:-1]
        r.sendline(input[5][::-1].encode())

    else:
        r.sendline(b"c")

    lettera = r.recvline(1).decode().split(" ")
    print(lettera)
    if(lettera[6] != "captcha\n"):
        lettereFlag += lettera[6][:-1]
    
print(lettereFlag)
r.close()
