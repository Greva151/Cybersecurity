import numpy as np
from PIL import Image

im1 = Image.open("flag_enc.png")
im2 = Image.open("notflag_enc.png")

im1np = np.array(im1)*255
im2np = np.array(im2)*255

enc1 = np.bitwise_xor(im1np, im2np).astype(np.uint8)
#enc2 = np.bitwise_xor(im1np, enc1).astype(np.uint8)
Image.fromarray(enc1).save('flag.png')