from PIL import Image
import zipfile

def extract_bits_from_bmp(bmp_path):
    image = Image.open(bmp_path)
    width, height = image.size

    bits = []

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            bit = 0 if pixel == 0 else 1
            bits.append(str(bit))

    return bits

def bits_to_bytes(bits):
    return [int(''.join(bits[i:i+8]), 2) for i in range(0, len(bits), 8)]

def save_bytes_to_zip(bytes_data, zip_filename):
    with open(zip_filename, 'wb') as zip_file:
        zip_file.write(bytes(bytearray(bytes_data)))

if __name__ == "__main__":
    bmp_path = "bits.bmp"
    zip_filename = "output.zip"

    bits = extract_bits_from_bmp(bmp_path)
    bytes_data = bits_to_bytes(bits)
    save_bytes_to_zip(bytes_data, zip_filename)

    print(f"I bit estratti dall'immagine BMP sono stati salvati in {zip_filename}")
