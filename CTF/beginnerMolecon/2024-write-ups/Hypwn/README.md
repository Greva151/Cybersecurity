# Hypwn
**Author**: MrCarr & Dione <br> 
**Category**: Pwn<br>  
**Solves**: 4<br>

## Description

Pokemon battles that you cannot win in any way.

## How to run the server
To run the server you need [`docker`](https://docs.docker.com/get-started/get-docker/) installed. <br>
Then you can navigate to the `src` folder and run the command `docker compose up --build -d`. <br>
Now you can connect to the server by opening [`http://localhost:5003/`](http://localhost:5003/) in your browser. <br>
To shut down the server run the command `docker compose down`.

## Solution

Analyzing the binary with Ghidra, it is evident that the Pokemon's health is stored in a variable defined as a `char` (a single byte).

Additionally, we can observe that when Arceus recovers health using leftovers, the program does not perform any check to prevent the health from exceeding 100. By stalling with Snorlax and alternating correctly between `Protect` and `Recover`, it is possible to survive 10 turns against Arceus, causing Arceus to gain 3 HP from leftovers at the end of each turn. 

After 9 turns, Arceus's health will reach 127. In two's complement representation, the range of values for a single byte is [-128, 127]. On the 10th turn, when Arceus gains 3 more health points, the check to verify whether its health is less than 0 will return `true`, allowing the program to call the `win()` function that prints the flag.
