import time
import os

with open("paginas.txt","r") as f:
	links=f.readlines()
	for l in links:
		os.system( "wget "+l)
		time.sleep(20) 