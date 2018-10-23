import time
import os

l=ord("A")
while l<=ord("Z"):
	dir=("https://cuidateplus.marca.com/enfermedades/%1s.html"%(str(unichr(l))))
	os.system( "wget "+dir)
	time.sleep(10)
	l+=1