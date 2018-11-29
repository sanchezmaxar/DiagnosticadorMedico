import time
import gensim
import os
import collections
import smart_open
import random
import csv
import unicodedata

def read_corpus(fname, tokens_only=False):
	global etq
	# ignorar=open("stopwords-es-master/stopwords-es.txt","r").read().splitlines()
	ignorar=[]
	with open(fname,"r") as f:
		lineas=map(lambda x:[i for i in x.split("|",1)],f.read().splitlines())
		ind=0
		for row in lineas:
			if len(row)>1 and len(row[1])!=0:
				aux=unicodedata.normalize('NFKD',row[1]).lower()
				for i in ignorar:
					aux=aux.replace(" "+i+" "," ")
				if len(aux.split())>30:
					if tokens_only:
						yield gensim.utils.simple_preprocess(aux)
					else:
						yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(aux), [ind])
					etq[ind]=row[0]
					# input(ind)
					ind+=1

def splitInv(cad,caracteres,stopwords):
	arreglo=[]
	aux=""
	cad=cad.lower()+"."
	for c in cad:
		if c not in caracteres :
			if aux!="" and aux not in stopwords:
				arreglo.append(aux)
			aux=""
		else:
			aux+=c
	return arreglo


etq={}
# stopwords=open("stopwords-es-master/stopwords-es.txt","r").read().splitlines()
stopwords=[]
train_corpus = list(read_corpus("datosLimpios.csv"))
model = gensim.models.doc2vec.Doc2Vec(
	vector_size=100,
	min_count=2,
	window=4,
	# dm=1,
	dm_concat=1,
	# dbow_words=1,
	epochs=475,
	workers=16,
	# ns_exponent=0
	)
# train_corpus = list(read_corpus("../datos.csv"))
# model = gensim.models.doc2vec.Doc2Vec(
# 	vector_size=100,
# 	min_count=5,
# 	window=2,
# 	dm=0,
# 	dm_concat=1,
# 	# dbow_words=0,
# 	epochs=300,
# 	workers=16,
# 	ns_exponent=1.125
# 	)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
texto=splitInv(open("misSintomas.txt").read(),"qwertyuiopasdfghjklzxcvbnm",stopwords)
print(texto)
vector=model.infer_vector(texto)
sim=model.docvecs.most_similar([vector],topn=4)
for i in sim:
	print("Documento Similar %s %s: " % (etq[i[0]],i[1]))
# -
texto=splitInv(open("misSintomas2.txt").read(),"qwertyuiopasdfghjklzxcvbnm",stopwords)
print(texto)
vector=model.infer_vector(texto)
sim=model.docvecs.most_similar([vector],topn=4)
for i in sim:
	print("Documento Similar %s %s: " % (etq[i[0]],i[1]))

# -
texto=splitInv(open("misSintomas3.txt").read(),"qwertyuiopasdfghjklzxcvbnm",stopwords)
print(texto)
vector=model.infer_vector(texto)
sim=model.docvecs.most_similar([vector],topn=4)
for i in sim:
	print("Documento Similar %s %s: " % (etq[i[0]],i[1]))

