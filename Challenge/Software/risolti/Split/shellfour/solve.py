key = [10, 5, 0, 25, 4, 14, 21, 22, 8, 6, 2, 9, 11, 12, 13, 23, 19, 16, 15, 3, 20, 17, 24, 18, 1, 7]
strings = ['p4z', 'n0', 'fla', 'E}', 'c1O', 'r33', '3_1', 'nc4', '4_s', '13', '1_p', 'tr4', 'z4t', '3_O', 'o_p', 'm1c', 'u33', 'r11', '3f3', '1ac', '3l1', '1sc', '1at', '1_q', 'g{t', 'uOv']
flag=""
for i in range(25, -1, -1):
	flag+=strings[key.index(i)][::-1]
	print(flag[::-1])
print("".join([strings[key.index(i)][::-1] for i in range(25,-1,-1)])[::-1])
