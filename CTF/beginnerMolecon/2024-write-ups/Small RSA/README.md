# Small RSA
<b>Author</b>: [kyooz](https://bsky.app/profile/blahajpilled.bsky.social)<br>
<b>Category</b>: Crypto <br>
<b>Solves</b>: 12<br>

## Descritpion
This RSA service does not allow messages that are too big, this way your message can always be decrypted!

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 3333` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.

## Solution
We are provided with a RSA encryption oracle that only tells us if our message is too big, in particular it tells us if this message is greater than p.
This check makes the service vulnerable since one of the factors of N gets leaked. 

We first need to recover N since the public key is not given to us, to do this we can use a little trick:
we will ask to encrypt a number x to get back its ciphertext ct, then we calculate x**e by ourselves on the integers, we will obtain two different numbers that are equal modulo N. This means that their difference will be a multiple of N. By repeating this trick with different numbers and taking the GCD of the so calculated differences we can recover N.

$$ct \equiv x^e (\textrm{mod}\ N) \implies x^e - ct \equiv 0 (\textrm{mod}\ N)$$

After that we can easily recover p using a simple binary search, if the service tells us that our message is too big we decrease our high bound, otherwise we increase our low bound.