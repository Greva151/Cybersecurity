from PIL import Image, ImageDraw, ImageFont
import os
import random
import sys

def add_noise(image):
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x,y))
            p = tuple([(c - random.randint(0, 255)) % 256 for c in p])
            image.putpixel((x,y), p)

for i in range(256):
    img = Image.open('output.bin')
    print("image number = " , i)
    add_noise(img)
    random.seed(i)
    output_filename = f"images/tent{i}.png"
    img.save(output_filename)
    
