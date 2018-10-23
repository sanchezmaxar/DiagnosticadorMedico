import nltk
import sys  
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

def gethref(texto):
	buf=""
	cond=False
	salida=[]
	for lineas in texto:
		print(lineas.get("href"))
	return salida


dirBase="./paginasBase/"
l=ord("P")
while l<=ord("Z"):
	url = dirBase+str(chr(l))+".html"
	html_doc = open(url,"r").read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	link = soup.find_all('a')
	# print(link)
	print (gethref(link))
	input("borrar")
	os.system("clear")
	l+=1
	print("------------------------------------------------------Aqui-----------------")
# print(soup.get_text())