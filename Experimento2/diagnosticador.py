from gensim.models.keyedvectors import KeyedVectors
import sys
import csv
from utilidades import *
import numpy as np
from scipy import spatial

def printD(di):
	s = [(k, di[k]) for k in sorted(di, key=di.get, reverse=True)]
	print("\n".join(map(lambda x:" -> ".join(map(str,x)),s)))

def vectorPromedioDeTexto(words, model, num_features):
	# Funcion modificada de https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction
	featureVec = np.zeros((num_features,), dtype="float32")
	nwords=0
	for word in words:
		try:
			nwords = nwords+1
			featureVec = np.add(featureVec, model[word])
		except:
			pass #ignoramos la palabra que conocemos
	if nwords>0:
		featureVec = np.divide(featureVec, nwords)
	return featureVec

def predecirSimilaridad(vector1,vector2):
	return 1 - spatial.distance.cosine(vector1,vector2)


wordvectors_file_vec = 'fasttext-sbwc.3.6.e20.vec.gz'
cantidad = 100000
num_features=300
wordvectors = KeyedVectors.load_word2vec_format(wordvectors_file_vec, limit=cantidad)


corpus={}
with open('datos.csv',"r",newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		corpus[row[0]]=vectorPromedioDeTexto(textoALista(row[1]),wordvectors,num_features)
		# print(corpus[row[0]])


with open(sys.argv[1],"r") as f:
	sintomas=vectorPromedioDeTexto(textoALista(noCaracteresEspeciales(f.read())),wordvectors,num_features)

vectorDeSimilaridades={}
for nombre,enfermedad in corpus.items():
	vectorDeSimilaridades[nombre]=predecirSimilaridad(enfermedad,sintomas)

printD(vectorDeSimilaridades)