# Small Auth
<b>Author</b>: Rising<br>
<b>Category</b>: Crypto<br>
<b>Solves</b>: 9<br>

## Descritpion
This may look like a normal calculator program, but it seems like the creator has something to hide...

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 5102` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.

## Solution

### Challenge Overview

This challenge is a cryptographic protocol puzzle involving Diffie-Hellman key exchange and some hashing mechanics. Here's a breakdown of its core components:

1. **Password-Based Key Generation**:  
   - The server uses a password (secret) to derive a generator \( g \), calculated as \( g = \text{bytes\_to\_long(password)}^2 \mod p \), where \( p \) is a large prime number.
   
2. **Public Key Exchange**:  
   - The server generates a random private value \( a \) and computes the public key \( A = g^a \mod p \).  
   - The client is expected to send a corresponding public key \( B \), and the shared key \( k = B^a \mod p \) is derived.

3. **Challenge-Response Authentication**:  
   - The server sends a challenge consisting of two 16-byte values (\( opad \) and \( ipad \)) and a SHA-256-based construction dependent on the shared secret \( s \).
   - The client must correctly compute and return a response to prove knowledge of \( s \).

4. **Timeout Behavior**:  
   - If the client does not respond promptly, the server generates its own \( ipad \) and \( opad \), providing an opportunity to analyze the challenge-response mechanism.

The flag is revealed only after successful authentication, requiring precise emulation of the cryptographic operations.

---

### Path to the Solution

The solution exploits the Diffie-Hellman key exchange implementation and reuses public keys across two parallel connections. Here’s how:

#### 1. **Understanding the Challenge's Vulnerability**
The server computes the shared secret \( s \) as \( k = B^a \mod p \), where \( B \) is the public key sent by the client. However, the key generation is agnostic of which client it interacts with. By setting up two simultaneous connections with the server, the attacker can:

1. Extract \( A \) (server’s public key) from one session and \( B \) from another.
2. Exchange these public keys between the two sessions, fooling the server into deriving identical shared secrets for both sessions.

This exploits the lack of binding between the challenge and the client’s true identity.

---

#### 2. **Steps to Exploit the Protocol**

1. **Establish Two Connections**:
   - Start two simultaneous connections with the server (e.g., using the `pwn` library).
   - Retrieve the server’s public key \( A \) from the first session and \( B \) from the second session.

2. **Exchange Public Keys**:
   - Send \( B \) to the first session and \( A \) to the second session. This ensures both sessions derive the same shared secret \( k \).

3. **Intercept and Replay the Challenge**:
   - Wait for the challenge from the first session and forward it to the second session.
   - Retrieve the response from the second session and send it back to the first session.

4. **Extract the Flag**:
   - Upon successful authentication in the first session, the server reveals the flag.

---

### Full Solution Code

```python
from pwn import *
import re
import time
import os

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', '5002')

FLAG_REGEX = re.compile(r"ptm\{[a-zA-Z0-9_]+\}")

s1 = remote(HOST, PORT)
s1.recvuntil(b"public key: ")
pub_key1 = int(s1.recvline().strip().decode())
log.info(f"Received A: {pub_key1}")

s2 = remote(HOST, PORT)
s2.recvuntil(b"public key: ")
pub_key2 = int(s2.recvline().strip().decode())
log.info(f"Received B: {pub_key2}")

s1.sendline(str(pub_key2).encode())
time.sleep(5)
s2.sendline(str(pub_key1).encode())

s1.recvuntil(b"Here is your challenge:")
challenge1 = s1.recvline().strip().decode()
log.info(f"Received challenge1: {challenge1}")

s2.sendlineafter(b"challenge (hex):", challenge1.encode())
s2.recvuntil(b"Response: ")
response2 = s2.recvline().strip().decode()

s1.sendlineafter(b"Response? (hex):", response2.encode())
out = s1.recvall(1)

flag = FLAG_REGEX.search(out.decode()).group()
log.success(f"Flag: {flag}")
```