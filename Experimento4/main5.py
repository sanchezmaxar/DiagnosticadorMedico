import sys,traceback
import unicodedata
import pickle
import numpy as np
from scipy.spatial import distance
import time
from math import exp,log
# Código para limpiar el corpus
# with open(sys.argv[1],"r") as f:
# 	enf=map(lambda x:x.split("|",2),f.read().splitlines())
# 	#sin revisar
# 	salida=open(archPickle,"w")
# 	for i in enf:
# 		if len(i)>1 :
# 			if len(i[1])<500:
# 				mantener=input(i)
# 				if mantener!="n":
# 					salida.write("|".join(i[:2])+"\n")
# 			else:
# 				print("meto ",i)
# 				salida.write("|".join(i[:2])+"\n")



def tf(doc,p):
	return doc.count(p)/len(doc)


def idf(docs,p,th):
	cont=0
	for d in docs:
		if p in d:
			cont+=1
	if cont<th:
		return 0
	else:
		return log(len(docs)/cont,10)

def splitInv(cad,caracteres,stopwords):
	arreglo=[]
	aux=""
	cad=cad.lower()
	for c in cad:
		if c not in caracteres :
			if aux.rstrip('sao')!="" and aux not in stopwords:
				arreglo.append(aux.rstrip('sao'))
			aux=""
		else:
			aux+=c
	# print(arreglo)
	return arreglo

def trnDocs(rawdocs,stopwords):
	docs={}
	for e,d in rawdocs.items():
		docs[e]=splitInv(unicodedata.normalize('NFKD',d),"qwertyuiopasdfghjklzxcvbnm",stopwords)
	return docs

def getVoc(docs,th=1,th2=0.1):
	vocab=[]
	for d in docs:
		for p in d:
			if p not in [v[0] for v in vocab]:
				aux=idf(docs,p,th)
				# print(aux)
				if aux>=th2:
					vocab.append((p,aux))
	return vocab

def leer(corpus):
	with open(corpus,"r") as f:
		for line in f:
			yield line.split("|",1)


def doc2Vec(doc,vocab,funcion):
	with open("../Experimento3/stopwords-es-master/stopwords-es.txt","r") as f:
	    stopwords=f.read().splitlines()
	try:
		palabras=splitInv(unicodedata.normalize('NFKD',doc),"qwertyuiopasdfghjklzxcvbnm",stopwords)
	except Exception as e:
		print(e,end="\r")
		palabras=doc
	vector=[]
	for key,value in vocab:
		vector.append(tf(palabras,key)*funcion(value))
	# print(vocab)
	return np.array(vector).reshape(1,-1)

def crearVectores(archCorpus,archPickle,funcion):
	with open("../Experimento3/stopwords-es-master/stopwords-es.txt","r") as f:
	    stopwords=f.read().splitlines()
	ti=time.time()
	corpus=dict(leer(archCorpus))
	print("Corpus leido")
	docs=trnDocs(corpus,stopwords)
	print("Documentos normalizados")
	vocab=getVoc(docs.values(),2,0.1)
	print("Vocabulario obtenido")
	vectores=[(n,doc2Vec(d,vocab,funcion)) for n,d in docs.items()]
	print("Vectores obtenidos")
	print("Me tarde : ",time.time()-ti)
	pickle.dump([vectores,vocab],open(archPickle,"wb"))
	return [vectores,vocab]

def leerVectores(archPickle):
	return pickle.load(open(archPickle,"rb"))


def predecir(archSintomas,vectores,vocab,funcion):
	sintomas=open(archSintomas,"r").read()
	vector=doc2Vec(sintomas,vocab,funcion)
	docs=[]
	for n,v in vectores:
		# docs.append([n,distance.cdist( vector,v, 'wminkowski',w=np.random.rand(v.shape[0]))])
		# docs.append([n,distance.cdist( vector,v, 'matching')])
		# docs.append([n,distance.cdist( vector,v, 'braycurtis')])
		# docs.append([n,distance.cdist( vector,v, 'canberra')])
		# docs.append([n,distance.cdist( vector,v, 'chebyshev')])
		# docs.append([n,distance.cdist( vector,v, 'jaccard')])
		# docs.append([n,distance.cdist( vector,v, 'correlation')])
		# docs.append([n,distance.cdist( vector,v, 'sqeuclidean')])
		# docs.append([n,distance.cdist( vector,v, 'cityblock')])
		docs.append([n,distance.cdist( vector,v, 'cosine')])
		# docs.append([n,distance.cdist( vector,v, 'euclidean')])
	docs.sort(key=lambda x:x[1])
	return docs
funcion=lambda x:1/(1+exp(5*(1-x)))
try:
	vectores,vocab=leerVectores(sys.argv[1])
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
for d in dists:
	input(d)

