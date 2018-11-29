import nltk
import sys  
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from utilidades import *
import csv
import time 
csvfile=open("datos.csv","w",newline='')
dataWriter=csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

listaDeSecciones=["Síntomas"] #la informacion que deseamos sacar
dirBase="../"
# dirBase=""
for nombre in open(dirBase+"htmls.txt","r").read().splitlines():
	auxrow=[nombre]
	fhtml=open(dirBase+nombre).read()
	soup = BeautifulSoup(fhtml,'html.parser')
	secciones = soup.find_all('p',attrs={'data-adhere':'true'})
	acum=""
	for s in secciones:
		acum+=s.get_text()
	auxrow.append(noCaracteresEspeciales(acum))
	links = soup.find_all('a',attrs={'class':'subnav__list__item__link'})
	acum=""
	for l in links:
		if l.text.strip() in listaDeSecciones:
			aux=(l.get("href"))
			os.system("wget "+aux)
			time.sleep(10)
			secciones = soup.find_all('p',attrs={'data-adhere':'true'})
			for s in secciones:
				acum+=s.get_text()
	auxrow.append(noCaracteresEspeciales(acum))
	dataWriter.writerow(auxrow)


