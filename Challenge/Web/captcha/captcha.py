#Gregorio Maria Vallè 5^C Informatica 15/12/2023

from PIL import Image
import pytesseract
import requests
import os 

def download_image(url, save_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'xb') as f:
            f.write(response.content)
        print(f"immagine salvata = {save_path}")
    else:
        print(f"Errore durante il download dell'immagine. Codice di stato: {response.status_code}")

session = requests.Session() 

url = "http://captcha.challs.olicyber.it/"

r = session.get(url)

counterImage = 0

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

for i in range(100): 
    urlImage = "http://captcha.challs.olicyber.it/" + r.text[428: 493]
    
    print("urlImmagine = " + urlImage)

    save_path = f'./immagini/immagine{counterImage}.png'
    counterImage += 1 

    print("percorso immagine = " + save_path)

    download_image(urlImage, save_path)

    img = Image.open(save_path)

    text = pytesseract.image_to_string(img)
    
    print("testo immagine = " + text)
    
    dati = {"risposta" : f"{int(text):08d}"}
    
    print("messaggio che mando = " + str(dati))

    r = session.post(url = url + "next", data=dati)
    
    print(r.text)