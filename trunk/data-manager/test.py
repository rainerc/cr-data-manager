def contains(myString, myVal, caseInsensitive):
	print 'myString: %s' % myString
	print 'myVal: %s' % myVal
	if caseInsensitive == True:
		myString = str.lower(myString)
		myVal = str.lower(myVal)
	print 'myString: %s' % myString
	print 'myVal: %s' % myVal
		
	return myVal.strip() in myString

print contains("batman's",'Batman\'s',True)