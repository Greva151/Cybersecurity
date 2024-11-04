import pyshark 

cap = pyshark.FileCapture("flag-interceptor.pcap")

dizionario = {}

for p in cap: 
    if "data" in p: 
        dizionario.setdefault(p.ip.src, "")  # Inizializza con una stringa vuota se la chiave non esiste
        dizionario[p.ip.src] += bytes.fromhex(p.data.data).decode()[:-1]
        
for ip in dizionario:
    if dizionario[ip].startswith("flag{") and dizionario[ip].endswith("}"):
        print(dizionario[ip])
