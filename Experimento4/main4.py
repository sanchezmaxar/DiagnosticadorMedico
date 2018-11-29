#!/usr/bin/env python
# coding: utf-8

def leer(corpus):
	with open(corpus,"r") as f:
		for line in f:
			yield line.split("|",1)


def getData(coo_matrix,feature_names):
	puntos=[]
	nombres=[]
	for score,idx in zip(coo_matrix.data,coo_matrix.col):
		aux=feature_names[idx].rstrip('sao') 
		if aux not in nombres:
			puntos.append(score)
			nombres.append(aux)
		elif score>puntos[nombres.index(aux)]: #aqui podemos ver que tomo el tf más grande de todos
            #principal diferencia con el experimento 5
			puntos[nombres.index(aux)]=score
	tup=zip(nombres,puntos)
	return sorted(tup,key=lambda x: x[1],reverse=True)

import unicodedata
import numpy as np
            
def doc2Vec(doc,vocab,funcion):
	palabras=list(map(lambda x: unicodedata.normalize('NFKD',x).rstrip('sao'),doc.split()))
	vector=[]
	for key,value in vocab.items():
		vector.append(funcion(palabras.count(key))*value)
	return np.array(vector).reshape(1,-1)

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import time
from math import exp

def crearVectores(archCorpus,archPickle,funcion):
    # se usa un set de palabras que deben detenerse, lo encontré en este repo.
    # https://github.com/stopwords-iso/stopwords-es
	with open("../stopwords-es-master/stopwords-es.txt","r") as f:
	    stopwords=f.read().splitlines() 
	corpus=list(leer(archCorpus)) # leemos el corpus
	vectorizador=TfidfVectorizer(smooth_idf=True, #aplicamos un suavizado del idf, no afecta mucho al resultado
                                 use_idf=True, # usamos idf
                                 stop_words=stopwords, # le damos el set de palabras a deterner
                                 min_df=2, # queremos que las palabras aparezcan al menos en dos documentos
                                 #si cambiamos esto a 1, pone muchas palabras que solo hacen el programa mas lento
                                 strip_accents='ascii') # le aplica una normalización a las palabras
	palabras=vectorizador.fit_transform(map(lambda x:x[1],corpus)) #aqui se aplica el tf-idf
	feature_names=vectorizador.get_feature_names() #se obtine el vocab
	keywords=dict(getData(palabras.tocoo(),feature_names)) # obtenemos el vocab relacionado con sus tf-idf
	vectores={} 
	cont=0
	total=len(corpus)
	ti=time.time()
	for c in corpus: #para cada documentos c en el corpus
		vectores[c[0]]=doc2Vec(c[1],keywords,funcion) # se transforma a un vector
		print("llevo ",cont," de ",total,end="\r") # contamos cuantos lleva
		cont+=1
	print("Me tarde : ",time.time()-ti)
	pickle.dump([vectores,keywords],open(archPickle,"wb")) #lo guardamos en un pickle para despues
	return [vectores,keywords] #regresamos los vectores y el vocab

from scipy.spatial import distance

def predecir(archSintomas,vectores,vocab,funcion):
	sintomas=open(archSintomas,"r").read()
	vector=doc2Vec(sintomas,vocab,funcion)
	docs=[]
	for n,v in vectores.items():
		# docs.append([n,distance.cdist( vector,v, 'wminkowski',w=np.random.rand(v.shape[0]))])
		# docs.append([n,distance.cdist( vector,v, 'matching')])
		# docs.append([n,distance.cdist( vector,v, 'braycurtis')])
		# docs.append([n,distance.cdist( vector,v, 'canberra')])
		# docs.append([n,distance.cdist( vector,v, 'chebyshev')])
		# docs.append([n,distance.cdist( vector,v, 'jaccard')])
		# docs.append([n,distance.cdist( vector,v, 'correlation')])
		# docs.append([n,distance.cdist( vector,v, 'sqeuclidean')])
		# docs.append([n,distance.cdist( vector,v, 'cityblock')])
		docs.append([n,distance.cdist( vector,v, 'cosine')]) #es la que mejor sirve
		# docs.append([n,distance.cdist( vector,v, 'euclidean')])
	docs.sort(key=lambda x:x[1])
	return docs
import sys
funcion=lambda x:1/(1+exp(5*(1-x)))
try:
	vectores,vocab=pickle.load(open(sys.argv[1],"rb"))
	ti=time.time()
	dists=predecir(sys.argv[2],vectores,vocab,funcion)
	print("Me tarde : ",time.time()-ti)
except Exception as e:
	print(e)
	try:
		vectores,vocab=crearVectores(sys.argv[1],sys.argv[2],funcion)
		dists=predecir(sys.argv[3],vectores,vocab,funcion)
	except Exception as ex:
		print(ex)
		traceback.print_exc(file=sys.stdout)
		print("Debes dar un archivo donde esten los vectores y los sintomas o el corpus y donde quieres guardar los vectores y los sintomas")
		print("ejemplo:\tpython3 main.py datosLimpios.csv vectores.pkl misSintomas.txt\n\t\tpython3 main.py vectores.pkl misSintomas.txt" )
		exit()

for i in range(10):
	print(dists[i])
