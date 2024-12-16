# Susculator
<b>Author</b>: lostGino04<br>
<b>Category</b>: Reverse<br>
<b>Solves</b>: 41<br>

## Descritpion
This may look like a normal calculator program, but it seems like the creator has something to hide...


## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 7070` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.


## Solution
In the executable you can find an hash function which can be solved using z3. This gives out the number `3141592653`. If then we put that number in the prompt, the program prints the flag.