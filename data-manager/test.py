def containsAnyOf(theList, theListDelimiter, checkThese, theCheckDelimiter):
	
	##
	myWords = str.split(theList, theListDelimiter)
	toCheck = str.split(checkThese, theCheckDelimiter)
	for word in myWords:
		if word in toCheck:	return True
		
	return False
	
print containsAnyOf('halt,stop','hat,stop,hugo',',')
