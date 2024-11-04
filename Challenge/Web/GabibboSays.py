from requests import *

s = Session()
parametri = {"gabibbo" : "angry"}
r = s.post("http://gabibbo-says.challs.olicyber.it/", data = parametri)

print(r.text)