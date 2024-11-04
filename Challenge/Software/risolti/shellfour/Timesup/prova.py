


#flag{tl_placcl0_n0_3f3u0v4_str4p4zz4t3_0o_pr333f3rlllscl_qu333l13_lnc4mlclatE}

array = [0x0a, 0x05, 0x00, 0x19, 0x04, 0x0e, 0x15, 0x16, 0x08, 0x06, 0x02, 0x09, 0x0b, 0x0c, 0x0d, 0x17, 0x13, 0x10, 0x0f, 0x03, 0x14, 0x11, 0x18, 0x12, 0x01, 0x07]

i = 0

dizionario = {}

stringa = "p4zn0_flaE}cl0r333_lnc44_sl3_l_ptr4z4t3_0o_plcu33rll3f3lac3l1lsclatl_qg{tu0v"

print(stringa[30])

while i < len(array):
    dizionario[array[i] * 3] = i
    i += 1
   
flag = [] 
print(dizionario)
for chiave in dizionario:
   flag.insert(chiave, stringa[dizionario[chiave]])
   flag.insert(chiave + 1, stringa[dizionario[chiave] + 1])
   flag.insert(chiave + 2, stringa[dizionario[chiave] + 2])
   print(dizionario[chiave])
   print(chiave)
   print(stringa[dizionario[chiave]])
   
   
print(flag)

#fla

'''

2 = 0
24 = 3
10 = 6
19 = 9
1 = 15
9 = 18
25 = 21
4 = 12
13 = 36
18 = 45
14 = 39
16 = 57
21 = 51
17 = 48
6 = 63
11 = 27
8 = 24
5 = 42
12 = 33
0 = 30
3 = 75
23 = 54
20 = 60
15 = 69
7 = 66
22 = 72


'''