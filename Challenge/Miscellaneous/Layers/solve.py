
binary = ""

for _ in range(56): 
    f = open(str(_), "r")
    binary += f.read()
    
integer = bytes.fromhex(hex(int(binary, 2))[2:]).decode()
start_flag = "INTEGRITY{"
print(len(integer))

               