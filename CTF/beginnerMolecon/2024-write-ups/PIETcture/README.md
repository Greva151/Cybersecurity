# PIETcture
**Author**: [TagBot](https://discordapp.com/users/596275829215068191) <br>
**Category**: Misc <br>
**Solve**: 14 <br>

## Description
Paint by Numbers? Or perhaps, compute by pixels?

## Solution
As the description of the challenge suggests, the image is not only an incredible work of art (which took me longer than I'm willing to admit,) but also a real executable program. 

By googling "pixel programming language" or something similar, it's pretty easy to read about the esolang "PIET" named after the famous abstract painter Piet Mondrian. The challenge name hints strongly that this is the right way to go about the challenge.

By googling more specifically "PIET programming language", the first (or at least one of the first) search results link to https://esolangs.org/wiki/Piet, which contains a brief description of the programming language and explains how it works. The bottom of the page contains external resources including the url to the official page of the language (https://www.dangermouse.net/esoteric/piet.html) and a list of tools related to development and execution of the code.

At the time of writing this, some of the tools don't seem to work at all, some work to a certain extent and others work surprisingly well. For the sake of testing, I used npiet (https://www.bertnase.de/npiet/) and MasterPiets (https://gabriellesc.github.io/piet/).

After installing npiet and running the challenge with
> ./npiet PIETcture.png 
> 
or importing the attached **PIETcture.png** in **MasterPiets** and running it, the code is going to ask for a password. By trying to guess the password the code is probably going to print "Nope..." (unless some ungodly guessing skills).

All the executable does under the hood is push the flag onto the stack, print 'Password?', push the password onto the stack, and then ask for input characters one by one, comparing them with the stored password. If they all match the flag is going to get printed, otherwise the executable just prints: "Nope..." as seen before.

The password, as well as the flag, can easily be obtained by looking at the stack trace since PIET is a stack based programming language and both strings are stored on the stack in reverse order, with each character represented by its ASCII value. This can be done with MasterPiets or by running the code in npiet with the '-t' flag to enable stack tracing. When using npiet the last output before the code pauses waiting for input should look like this:
```
trace: step 1085  (24,9/l,r dY -> 23,9/l,r nY):
action: pop
trace: stack (51 values): 65 98 115 116 114 97 99 116 67 48 100 49 110 103 0 112 116 109 123 49 95 115 104 48 117 108 100 95 104 52 118 51 95 98 51 99 48 109 51 95 52 110 95 52 114 116 49 115 116 125 0
```
By copying the values and using cyberchef or python to convert from decimal we get the flag and the password. We can now just copy the flag and get the points or use the password when prompted by the executable. This time the password check is going to get passed and the flag will be printed.

P.S.: The Author tag with the value **Not Mondrian** found in the metadata is just another easter egg hinting to Piet Mondrian.
