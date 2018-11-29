import nltk
import sys  
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

def gethref(texto,lim1,lim2):
	cond=False
	salida=[]
	for lineas in texto:
		aux=lineas.get("href")
		if aux==lim1:
			cond=True
		elif cond:
			if aux==lim2:
				return salida
			else:
				salida.append(aux)
	return salida

archivo=open(sys.argv[1],"w")
limites=["https://www.onmeda.es/enfermedades/enfermedades__xyz.html","https://www.onmeda.es/enfermedades/enfermedades_frecuentes.html"]
dirBase="./paginasBase/enfermedades__"
letras=["az"]+[chr(i) for i in range(ord("b"),ord("w")+1)]+["xyz"]
for l in letras:
	url = dirBase+l+".html"
	html_doc = open(url,"r").read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	link = soup.find_all('a')
	archivo.write( "\n".join(gethref(link,limites[0],limites[1])))
