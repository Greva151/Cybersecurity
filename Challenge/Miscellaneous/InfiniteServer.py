#Gregorio Maria Vallé 4^C Informatica 08/07/2023

from selenium import webdriver
from selenium.webdriver.common.by import * 

driver = webdriver.Chrome()

driver.get("http://infinite.challs.olicyber.it/")

while True:
    
    testo = driver.page_source
    split = testo.split()
    print(testo)

    if "ART" in testo:
        index = split.index("colore")
        colore = split[index + 1][:-5]
        element = driver.find_element(By.ID, colore)
        element.click()
        
    elif "MATH" in testo:
        
        index = split.index("fa")
        n1 = int(split[index + 1])
        n2 = int(split[index + 3][:-5])
        risposta = n1 + n2 
        element = driver.find_element(By.NAME,"sum")
        element.send_keys(str(risposta))
        element = driver.find_element(By.XPATH, "//form[@id='myform']/input[2]")
        element.click()
        
    elif "GRAMMAR" in testo:
        
        index = split.index("ci")
        lettera = split[index-1][1:2]
        print(lettera)
        index = split.index("parola")
        parola = split[index+1][1:-6]
        print(parola)
        risposta = parola.count(lettera)
        print(risposta)
        element = driver.find_element(By.ID,"letter")
        element.send_keys(str(risposta))
        element = driver.find_element(By.NAME,"submit")
        element.click()

input()

driver.quit()
