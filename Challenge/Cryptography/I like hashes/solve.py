import hashlib

with open('ct.txt', 'r') as file:
    for line in file:
        line = line[:-1]
        for i in range(32, 127):
            lettera = chr(i)
            if line == hashlib.sha256(lettera.encode()).hexdigest():
                print(lettera, end="")
                break
print("}")

