#!/usr/bin/env python3

# La tabella di sostituzione (array S) usata per la cifratura
S = [120, 41, 183, 252, 96, 74, 43, 182, 251, 56, 248, 121, 13, 84, 245, 54, 178, 235, 207, 254, 45, 58, 2, 89, 200, 101, 133, 249, 119, 142, 239, 211, 50, 29, 77, 72, 107, 230, 104, 229, 241, 11, 57, 215, 155, 234, 247, 113, 122, 130, 22, 12, 212, 88, 49, 174, 176, 206, 243, 100, 255, 106, 87, 115, 195, 188, 194, 123, 161, 62, 48, 216, 98, 173, 137, 78, 213, 36, 240, 47, 65, 236, 85, 18, 166, 170, 28, 204, 148, 125, 232, 189, 0, 196, 64, 242, 16, 80, 150, 169, 167, 165, 220, 168, 7, 23, 21, 141, 30, 93, 26, 68, 35, 70, 9, 218, 69, 158, 105, 180, 110, 60, 83, 186, 112, 172, 44, 27, 205, 76, 198, 99, 225, 222, 184, 154, 102, 193, 237, 118, 139, 157, 61, 92, 146, 253, 246, 1, 4, 24, 79, 10, 228, 97, 187, 33, 227, 15, 191, 59, 192, 40, 156, 201, 250, 67, 210, 114, 19, 94, 73, 214, 163, 164, 90, 226, 20, 203, 231, 82, 197, 134, 221, 199, 219, 42, 103, 190, 147, 144, 17, 108, 52, 31, 3, 6, 209, 66, 51, 208, 217, 153, 86, 14, 171, 224, 37, 127, 136, 151, 140, 55, 131, 95, 38, 5, 75, 185, 202, 149, 145, 39, 160, 25, 244, 46, 126, 138, 181, 177, 53, 117, 116, 128, 238, 32, 135, 111, 109, 143, 34, 124, 223, 233, 8, 71, 152, 63, 175, 159, 129, 179, 91, 132, 81, 162]
ss = 105

# Il testo cifrato fornito
encrypted_hex = "e2e28e08c70987875fe072511113024c117b7264bb4ce2bb0287083b4cbabe4c67eb38114cf45109a8724c3b64134cbebebef4f4f438bef438bef4bebe383838be38bef488"
encrypted_bytes = bytes.fromhex(encrypted_hex)

# Calcola l'inverso della tabella S
inverse_S = {v: k for k, v in enumerate(S)}

# Funzione per decriptare un byte
def decrypt_byte(encrypted_byte, initial_value):
    current_value = encrypted_byte
    counter = 0
    while current_value != initial_value:
        current_value = inverse_S[current_value]
        counter += 1
    return counter

# Decripta ogni byte cifrato
decrypted_bytes = []
for byte in encrypted_bytes:
    decrypted_bytes.append(decrypt_byte(byte, ss))

# Converti i byte decriptati in una stringa
flag = bytes(decrypted_bytes).decode()

print("Flag decriptata:", flag)
