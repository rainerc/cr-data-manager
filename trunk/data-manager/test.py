from utils import *
import System
from System import String

comp = comparer()

def notContainsAnyOf(myString,myVal,caseInsensitive):
	theVals = myVal.strip(',').split(',')
	myString = String.Trim(myString)
	for word in theVals:
		word = String.Trim(word)
		if caseInsensitive == True:
			if str.find(str.lower(myString),str.lower(word)) >= 0: return False
		else:
			if str.find(myString,word) >= 0: return False
	return True

print notContainsAnyOf("Hugo ","Marvel Cosmic,Hugo,Otto",True)