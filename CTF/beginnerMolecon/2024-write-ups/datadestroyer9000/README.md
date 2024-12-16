# datadestroyer9000
<b>Author</b>: [kyooz](https://bsky.app/profile/blahajpilled.bsky.social)<br>
<b>Category</b>: Crypto <br>
<b>Solves</b>: 8<br>

## Descritpion
No one will be able to recover my secrets thanks to my new data destroyer!

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 5555` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.

## Solution
The challenge consists of a service that allows us to "destroy" some sequence of bytes, the problem is that the operations done on the data are completely reversible and they are also very easy to reverse. 
Our sequence of bytes first gets divided into chunks of 64 bytes, the same one time pad gets applied to all of these chunks and then each chunk gets divided in blocks of size 8, each byte in these blocks gets then scrambled with some permutation. These permutations are the same over different chunks but even if they were not, it would still be possible to revert them.

So how can we find which one time pad and permutations got used?
Because the one time pad is always the same, we can xor two ciphertexts in order to get rid of the one time pad, at this point we just need to recover the permutations that got used.
We can notice that after we xor two ciphertexts, we don't exactly get the xor of their two plaintexts, but instead the bytes of their xor after they got scrambled. In this way we can recover the permutations used by the service to scramble our data.

A pair of plaintext blocks that makes it very easy to recover a permutation is **00 00 00 00 00 00 00 00** and **00 01 02 03 04 05 06 07**, after we xor their two corresponding ciphertexts we can map the starting and ending positions of each byte, successfully recovering the permutation used on the block
