from zipfile import ZipFile
from pwn import *


f = open("rockyou.txt", "r")

lista = []

for i in range(10_000):
    lista.append(f.readline()[:-1])

for i in range(100, 0, -1):
    file = str(i) + ".zip"
    
    with ZipFile(file) as zip:
        for c in range(10_000):
            try:
                zip.extractall(pwd = bytes(lista[c], 'utf-8'))
                print(lista[c])
                break
            except:
                continue
f.close()
