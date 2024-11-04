from requests import *

payload = {"username": "admin" , "password": "admin"}
s = Session()
r = s.post("http://web-11.challs.olicyber.it/login", json = payload)

cookies = r.cookies["session"]
csrf = r.json()["csrf"]
res = ""
for i in range(4):
    params = {"csrf" : csrf, "index": i}
    r = s.get("http://web-11.challs.olicyber.it/flag_piece", params=params)
    csrf = r.json()["csrf"]
    res += r.json()["flag_piece"]

print(res)