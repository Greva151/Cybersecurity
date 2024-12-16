# Identity Theft
**Author**: [Mrdega](https://discordapp.com/users/684707774831001600) <br>
**Category**: Crypto <br>
**Solve**: 8 <br>

## Description
Can you deceive Alice into revealing all her secrets?

## How to run the server
To run the server you need [`docker`](https://docs.docker.com/get-started/get-docker/) installed. <br>
Then you can navigate to the `src` folder and run the command `docker compose up --build -d`. <br>
Now you can connect to the server by opening [`http://localhost:31338/`](http://localhost:31338/) in your browser. <br>
To shut down the server run the command `docker compose down`.

## Solution

### Overview
We are presented with two chats, one between Alice and Bob and the other in which we can replace Bob and talk with Alice. We see Alice and Bob establish a Diffie-Hellman connection to encrypt their messages and we can do the same with Alice, following her instructions.<br>
The box on the right is used to convert the shared key we calculate in the DH exchange to a key for encrypting and decrypting messages.

### Exploit
First we can execute a Diffie-Hellman key exhange with Alice, use the converter to get the **key** and decrypt the message she sends us with **AES-ECB**. Then having the possibility to insert a custom generator **g**, we can guess Alice keeps always the same **private key** and retrieve their **shared key** by setting **g** as **Bob's public key** and the prime number **p** as the one used in their chat. This way using the converter, we can get the **key** to decrypt the message Alice sent Bob with **AES-ECB**.<br>
We find the first part of the flag in Alice's message to Bob and the second part in Alice's message to us.