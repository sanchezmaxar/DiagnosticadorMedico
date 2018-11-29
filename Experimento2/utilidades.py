from unicodedata import normalize
import re
def noCaracteresEspeciales(texto):
	# -> NFD y eliminar diacríticos
	
	# -> NFC
	texto=re.sub('\W',' ',texto)
	# texto = normalize( 'NFC', texto)
	# print(normalize('NFKC',texto))
	return texto.lower()

def textoALista(texto):
	listaaux=texto.split()
	listaaux.sort()
	lista=[]
	for i in listaaux:
		if i not in lista:
			lista.append(i)
	return lista

print( noCaracteresEspeciales("holá , como estas"))