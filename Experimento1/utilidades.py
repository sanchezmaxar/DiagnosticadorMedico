from unicodedata import normalize
import re
def noCaracteresEspeciales(texto):
	# -> NFD y eliminar diacríticos
	texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", texto), 0, re.I
    )

	# -> NFC
	texto=re.sub('\W',' ',texto)
	texto = normalize( 'NFC', texto)
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