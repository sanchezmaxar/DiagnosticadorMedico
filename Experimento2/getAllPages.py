import time
import os

with open("paginas.txt","r") as f:
	links=f.readlines()
	for l in links:
		try:
			open(l[:-1].rsplit("/",1)[1],"r")
		except:
			os.system( "wget "+l)
			time.sleep(10) 