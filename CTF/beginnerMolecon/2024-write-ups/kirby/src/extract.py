from PIL import Image

with Image.open('chall.gif') as im:
    for i in range(im.n_frames):
        im.seek(i)
        im.save(f'{i}.png')
