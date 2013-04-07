import System
from System import String
from System.IO import File
from System.Windows.Forms import MessageBox
import re
import globalvars
#import str

class comparer(object):
	"""description of class"""

	def inList(self,myString,myVal,caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		theVals = myVal.strip(',').split(',')
		for word in theVals:
			if String.Trim(word) == String.Trim(myString): return True
		return False

	def containsAnyOf(self, myString, myVals,caseInsensitive):
		theVals = myVals.strip(',').split(',')
		for word in theVals:
			if caseInsensitive == True:
				if str.find(str.lower(myString),str.lower(word)) >= 0: return True
			else:
				if str.find(myString,word) >= 0: return True
		return False
	
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

	def containsAllOf(self, myString, myVals,caseInsensitive):
		theVals = myVals.strip(',').split(',')
		for word in theVals:
			if caseInsensitive == True:
				if str.find(str.lower(myString),str.lower(word)) < 0: return False
			else:
				if str.find(myString,word) < 0: return False
		return True

	def contains(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return str.find(myString,myVal) >= 0
	
	def containsNot(self, myString, myVal, caseInsensitive):#
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)		
		return str.find(myString,myVal) < 0
	
	def equals(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString == myVal

	def startsWith(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString.startswith(myVal)
	
	def startsWithAnyOf(self, myString, myVals, caseInsensitive):
		theVals = myVals.strip(',').split(',')
		for word in theVals:
			if caseInsensitive == True:
				if String.StartsWith(lower(myString),lower(word)):
					return True
			else:
				if String.StartsWith(myString,word):
					return True
		return False
		
	
	def less(self,myString,myVal,caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString < myVal

	def lessEq(self,myString,myVal,caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString <= myVal

	def greater(self,myString,myVal,caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString > myVal

	def greaterEq(self,myString,myVal,caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString >= myVal

	def notEq(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString <> myVal

def nullToZero(s):
	if String.Trim(str(s)) == '':
		return 0
	return s

def multiValueAdd(myList, myVal):
	myVal = str.Trim(str(myVal))
	newList = []
	theList = myList.strip(',').split(',')
	for l in theList: 
		l = str.Trim(l)							
		if l <> '': newList.Add(l)								# eliminate Null values
	if newList.count(myVal) > 0: return ','.join(newList)		# item already in list?
	newList.append(myVal)										# otherwise append newVal
	return ','.join(newList)

def multiValueReplace(myList, oldVal, myVal):
	oldVal = String.Trim(str(oldVal))
	myVal = String.Trim(str(myVal))
	newList = []
	theList = myList.strip(',').split(',')
	for l in theList:
		l = String.Trim(l)
		if l == oldVal: l = myVal
		if newList.count(l) == 0:
			newList.Add(l)
	return ','.join(newList)

def multiValueRemove(myList, myVal):
	myVal = String.Trim(str(myVal))
	theList = myList.strip(',').split(',')
	newList = []
	for l in theList:
		l = String.Trim(l)
		if l <> myVal:
			newList.Add(l)
	return ','.join(newList)

class parser(object):
	
	
	pass

def validate(s):
	'''
	validates the current line in the configuration for basic syntax errors
	if everything ok it returns the line
	else it returns the line prefixed with '# invalid expression'

	'''
	s = String.Trim(s)
	if not len(s) > 0:
		return ''

	p = re.compile('(<{2}|#)+.*')
	m = p.search(s)
	if m:
		pos = m.start()
	else:
		pos= -1
	if s [0] <> '#':
		if not (String.StartsWith(s,'<<') and String.EndsWith(s,'>>')):
			return '# invalid expression: %s' % s
		if str.count(s, '=>') <> 1:
			return '# invalid expression: %s' % s
		if str.count(s, '<<') <> str.count(s, '>>'):
			return '# invalid expression: %s' % s
		if str.count(s, '<<') > str.count(s,':'):
			return '# invalid expression: %s' % s
		if pos > 0:
			return s [pos:]
	if s[0] == '#' or s[0:2] == '<<':
		return s
	else:
		return '# invalid expression: %s' % s

def readDataFile(theFile):
	s=[]
	if theFile == globalvars.DATFILE:
		if File.Exists(globalvars.DATFILE):
			File.Copy(globalvars.DATFILE, globalvars.BAKFILE, True) # just in case something bad happens
			s = File.ReadAllLines(globalvars.DATFILE)
		elif File.Exists(globalvars.SAMPLEFILE):
			s = File.ReadAllLines(globalvars.SAMPLEFILE)
	else:
		if File.Exists(theFile):
			s = File.ReadAllLines(theFile)
		else:
			return str('')

	tmp = str('')
	for line in s:
		tmp += line + System.Environment.NewLine
	if len(s) == 0 and theFile == globalvars.LOGFILE:
		tmp = 'Your criteria matched no book. No data was touched by the Data Manager.'
	return tmp

def writeDataFile(theFile, theText):
	'''
	writes the context of the configurator window to a file
	'''
	s = str.split(str(theText),'\n')
	tmp = str('')
	errlines = 0
	for line in s:
		s2 = validate(str(line))	# some basic validation
		if s2 <> '':
			# using System.Environment.NewLine instead of '\n'
			# to make the file easier to edit with external tool like Notepad
			#tmp += validate(str(line)) + '\n'
			tmp += validate(str(line)) + System.Environment.NewLine
			if String.StartsWith(str(line), '# invalid expression'):
				errlines += 1
	if len(theText) > 0:
		File.WriteAllText(theFile, tmp)
	else:
		MessageBox.Show('File not written (0 Byte size)')
	if errlines > 0:
			MessageBox.Show('Your rules contained %d syntax errors. Those were marked with \"# invalid expression\"' % errlines)

	if not File.Exists(globalvars.CHKFILE):
		File.Create(globalvars.CHKFILE)
	return