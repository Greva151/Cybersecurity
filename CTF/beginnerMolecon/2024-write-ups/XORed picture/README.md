# XORed picture
<b>Author</b>: Vic<br>
<b>Category</b>: Misc, Crypto<br>
<b>Solves</b>: 51<br>

## Descritpion
My friend has sent me a pic, but I can't seem to open it. They said it has been **XOR**'d or something...

## Solution

### Understanding the source code
We are given a `chall.py` file that takes a `flag.png` file, xors it with a random key and saves the result in a `flag_enc.png` file.

The python script opens the `flag.png` file as a generic binary file, saves its contents in a variable `pt` and then calls the pwntools function `xor` on it. This way each byte in the original file is xored with a byte of the `key`.

For this reason, if we try to open the `flag_enc.png` file we get an error: it is not a valid png file anymore, because it has been xored with some random data!

Actually, we can't even be sure it was a png file before being xored, but it is a reasonable assumption based on the extension in the file name.

### Solution
Since the file has been xored byte by byte, and we assume that it was a png file, we can retrieve some information about the plaintext, that may help us.

- **Magic numbers**: the first few bytes of a file identify its format. On wikipedia we can find a list of the magic numbers for the most common file formats (https://en.wikipedia.org/wiki/List_of_file_signatures) and we find out that our `flag.png` file must start with `89 50 4e 47 0d 0a 1a 0a`.

This is quite a helpful information, but it's not enough, because we only know 8 bytes of the plaintext and the key is 16 bytes long. We must search for more information about the png file format.

- **PNG file format**: We can easily find the information we are looking for (https://en.wikipedia.org/wiki/PNG#Critical_chunks): the next 8 bytes must be `IDHR` (name of the first chunk) followed by the dimension of the first chunk (13 bytes).

Now we know the first 16 bytes of the plaintext, thanks to the properties of the xor operator, we can xor these 16 bytes against the first 16 bytes of the ciphertext we are given, and we will get the key. 

Then we can use the key to decrypt the whole `flag_enc.png` file.

### Code
```python
from pwn import xor

fin = open("flag_enc.png", "rb")
fout = open("flag_dec.png", "wb")

ct = fin.read()

magic_number = bytes.fromhex("89504e470d0a1a0a")
first_chunk_type = b'IHDR'
first_chunk_size = (13).to_bytes(4, "big")

known_pt = magic_number + first_chunk_size + first_chunk_type
key = xor(known_pt, ct[:len(known_pt)])

print(key)

fout.write(xor(ct, key))
fin.close()
fout.close()
```