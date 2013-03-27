def containsAnyOf(theList, theListDelimiter, checkThese, theCheckDelimiter):
	
	##
	myWords = str.split(theList, theListDelimiter)
	toCheck = str.split(checkThese, theCheckDelimiter)
	for word in myWords:
		if word in toCheck:	return True
		
	return False


def multiValueAdd(myList, myVal):
	s = str(myVal)
	
	# theList = str.Replace(myList,', ',',').split(',')
	theList = myList.split(',')
	print theList
	for l in theList:
		l = str.Trim(l)
	if theList.count(s) > 0:		# item already in list?
		return myList
	if len(theList) > 0 and theList[0] <> '':
		theList.append(s)
		s =  ','.join(theList)
	return s
	
# print containsAnyOf('halt,stop','hat,stop,hugo',',')


multiValueAdd('scanlation','scanlation')
raw_input('key')

