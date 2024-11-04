stringa = "27893459dc8772d66261ff8633ba1e5097c10fba257293872fd2664690e975d2015fc4fd3c"

for i in range(255):
    var = bytes.fromhex(stringa)[0] ^ i
    if var == ord("f"):
        print(i)
        
for i in range(255):
    var = bytes.fromhex(stringa)[1] ^ i
    if var == ord("l"):
        print(i)

for i in range(255):
    var = bytes.fromhex(stringa)[2] ^ i
    if var == ord("a"):
        print(i)
        
for i in range(255):
    var = bytes.fromhex(stringa)[3] ^ i
    if var == ord("g"):
        print(i)

for i in range(255):
    var = bytes.fromhex(stringa)[4] ^ i
    if var == ord("{"):
        print(i)
        
print((bytes([65, 229, 85, 62, 167]) + bytes([1])).hex())

def xor(a, b):
    return bytes([ x ^ y for x,y in zip(a,b) ])

for i in range(255):
    print(xor(bytes.fromhex("27893459dc8772d66261ff8633ba1e5097c10fba257293872fd2664690e975d2015fc4fd3c"), (bytes([65, 229, 85, 62, 167]) + bytes([i]))*7))
    
#flag{1337_X0r_Kn0wN_pL41n73x7_47TacK}