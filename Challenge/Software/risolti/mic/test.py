transformed =   "QE4U8PzcV9oTx6WNkhb0ZYg3s2afRIdjX157"                 
original =      "1Qa2Ws3Ed4Rf5Tg6Yh7Uj8Ik9oZx0PzXcVbN"
psw =           "SP3CCSPXE6ZUC2HC9HJLDZX52UN5H8AO5WDZ"


dizionario = {} 

for i in range(len(transformed)): 
    dizionario[i] = original.index(transformed[i])

flag = [''] * 36

for old, new in dizionario.items(): 
    print(f"index = {old}; value = {new}")
    flag[new] = psw[old]
    
flag = "".join(flag)

print(flag)
