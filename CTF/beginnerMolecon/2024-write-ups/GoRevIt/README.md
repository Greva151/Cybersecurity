# GoRevIt

<b>Author</b>: [Schrödy](https://github.com/AndreaGordanelli)<br>
<b>Category</b>: Reverse, Misc<br>
<b>Solves</b>: 0<br>

## Descritpion

I want to make my car go faster, but first I have to find the keys

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 3240` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.

## Solution

The challenge gives a shared object and a connection to a simulated UDS, to obtain the flag
we have to solve the seed&key challenge, the function is in the provided shared object.
We can connect to the remote server using netcat

Here we can insert, inspect, and send a UDS packet, we can start requesting the seed by pressing **1** to insert the packet `2701` and then sending it with the number **3**
After we receive the seed we can process it and send it to obtain the flag.
The best way to obtain the key given the seed is by using the provided [Shared Object](https://en.wikipedia.org/wiki/Shared_library) file so you won't need to reverse the whole function, but only find the name. Here's a little python snippet to load the SO and get the key given the seed:
```python
import ctypes

lib = ctypes.CDLL('./keygen.so')
lib.fromSeedToKey.argtypes = [ctypes.c_char_p]
lib.fromSeedToKey.restype = ctypes.c_char_p

def genKey(seed: str) -> str:
    result = lib.fromSeedToKey(seed.encode('utf-8'))
    output = ctypes.string_at(result).decode('utf-8')
    return output

s = input("Seed (in hex): ").strip('0x')
print("Key: ", genKey(s))
```
using the previous step: pressing **1**, insert the packet `2702 + key`, and then pressing **3**, this should give us the flag.
