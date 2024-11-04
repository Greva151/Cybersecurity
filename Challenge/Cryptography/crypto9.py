def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


a = 187
b = 199
mcd, x, y = extended_gcd(a,b)

print(x,y,mcd )

print(pow(18, -1, 55))