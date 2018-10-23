import nltk
import sys  
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from utilidades import *
import csv

csvfile=open("datos.csv","w",newline='')
dataWriter=csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

listaDeSecciones=["Síntomas"] #la informacion que deseamos sacar
dirBase="./paginasEspecificas/"
# dirBase=""
for nombre in open(dirBase+"htmls.txt","r").read().splitlines():
	# input("hola")
	# print(nombre)
	fhtml=open(dirBase+nombre).read()
	soup = BeautifulSoup(fhtml,'html.parser')
	secciones = soup.find_all('h2',attrs={'class':'c'})
	ant=0
	act=0
	for s in secciones:
		if ant==0:
			pass
		else:
			if s.text.strip() in listaDeSecciones:
				html_aux=fhtml[ant:act]
				temp_soup=BeautifulSoup(html_aux,'html.parser')
				# print(temp_soup.get_text())
				dataWriter.writerow([nombre,noCaracteresEspeciales(temp_soup.get_text())])
		ant,act=act,fhtml.find(str(s))

