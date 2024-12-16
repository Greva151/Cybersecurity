# Locked Door
<b>Author</b>: [meni](https://github.com/menitz/)<br>
<b>Category</b>: Web, Crypto <br>
<b>Solves</b>: 79<br>

## Descritpion
In front of you stands a door with a digital terminal. Will you be able to open it?

## How to run the server
To run the server you need [`docker`](https://docs.docker.com/get-started/get-docker/) installed. <br>
Then you can navigate to the `src` folder and run the command `docker compose up --build -d`. <br>
Now you can connect to the server by opening [`http://localhost:5000/`](http://localhost:5000/) in your browser. <br>
To shut down the server run the command `docker compose down`.

## Solution

Looking at the home page, we find a "access_log" button that does not work. By analyzing the code, we find a disabled attribute, removing it allows us to access the "access_log" page.
```html
<button id="access_log_button" onclick="window.location.href='/.....'" disabled>Access Log</button>
```

On the page, there are some files with the download button that opens a login window. Inspecting the code, we find a comment that helps us understand that we need to perform an SQL injection.
```html
Password: 
<input type="password" name="password"><br> 
<!-- – remember to prevent sql injection – -->
```
By attempting an SQL injection using `' or 1=1 --`, we manage to gain access and download a `.pcap` file.
Opening the `.pcap` file, we find some TCP traffic where we can find the following information:
```
Protocol: RSA
n:149105804516152894583949786187504223437
e: 65537

Ciphertext: 76920112040626308839299220007728101947
```
By attempting to factorize $n$ with SageMath (for example using [SageMathCell](https://sagecell.sagemath.org/)), we find the factors $p$ and $q$. At this point, we can calculate $\phi=(p-1)\cdot(q-1)$, then $d=e^{-1} \mod \phi$ and the plaintext as $p=c^d \mod n$. We then find the code $12460119$ to enter on the homepage to find the flag.