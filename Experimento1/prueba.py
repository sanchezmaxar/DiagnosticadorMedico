di={1:2,3:2,32:1}
def printD(di):
	s = [(k, di[k]) for k in sorted(di, key=di.get, reverse=True)]
	print("\n".join(map(lambda x:" -> ".join(map(str,x)),s)))
printD(di)