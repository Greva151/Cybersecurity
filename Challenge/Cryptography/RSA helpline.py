def phi(p, q):
    #nel caso in cui il numero è un numero primo phi(n) è n - 1 
    return (p-1)*(q-1)

p = 17
q = 13 
n = p * q
m = 10
e = 7
d = 0

print("n = ", n)

print("m = ", m)

numeroeurolo = phi(p,q) 
print("phi = ", numeroeurolo)

numeroCriptato = pow(m,e,n)

print("numero criptato = ", numeroCriptato)

print(pow(e, -1, phi(p,q)))
# teorema di eurelo 
# se MCD(a,n) = 1   -->  a^phi(n) congruo = a^0 (mod n)
# m^(e*d) congruo 1 (mod n)  --> e * d = 1 (mod phi(n))
# d congruo e^-1 (mod phi(n))   <-- this 
# pow(e, -1, phi(p,q))