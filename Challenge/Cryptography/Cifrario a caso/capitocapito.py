import random

flagCriptata = open("cifrario_a_caso_output.txt", "r").read()

flagCriptata = bytes.fromhex(flagCriptata)

for i in range(255):
    stringa = []
    random.seed(i)

    for c in flagCriptata:
        lettera = c ^ random.randint(0, 255)
        stringa.append(lettera)
    try:
        print(bytes(stringa).decode())
    except:
        pass