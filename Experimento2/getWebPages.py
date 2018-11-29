# Programa actualizado para e experimento

import time
import os
import sys


l=["az"]+[chr(i) for i in range(ord("b"),ord("w")+1)]+["xyz"]
for i in l:
	dir=("https://www.onmeda.es/enfermedades/enfermedades__%s.html"%i)
	# print ("wget "+dir+ " -o  ./paginasBase/")
	os.system("wget "+dir)
	time.sleep(10)
