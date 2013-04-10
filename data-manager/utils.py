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
	
	
	def __init__(self):
		self.err = False
		self.error = ''
		
	def commentedLine(self, line):
		return '#\t------------%s#\tinvalid expression in next line (%s)%s#\t%s%s#\t------------' % (
			System.Environment.NewLine,self.error, System.Environment.NewLine, line, System.Environment.NewLine)
		
	def validate(self, s):
		'''
		validates the current line in the configuration for basic syntax errors
		if everything ok it returns the line
		else it returns the line prefixed with '# invalid expression'
	
		'''
		s = String.Trim(s)
#		print s
		if not len(s) > 0:
			self.err = False
		# check if line is comment
		if s.StartsWith('#@'):		# directive?
			self.err = False
			return
		if s.StartsWith('#'):		# comment?
			self.err = False
			return
		if s.StartsWith('<<'):	# valid rule
			if not String.EndsWith(s,'>>'):
				self.err = True
				self.error = 'missing >> at the end of rule'
				return
			if str.count(s, '=>') == 0:
				self.err = True
				self.error = 'missing => in rule'
				return
			if str.count(s, '=>') > 1:
				self.err = True
				self.error = 'more than one occurence of => in rule'
				return
			if str.count(s,'<<') <> str.count(s, '>>'):
				self.err = True
				self.error = 'count of << mismatches count of >>'
				return
			if str.count(s, '<<') > str.count(s,':'):
				self.err = True
				self.error = 'count of << mismatches count of :'
				return
			else:
				self.err = False
				self.error = ''
				return
		else:						# rule does not start with <<
			self.err = True
			self.error = 'rules must start with <<'
			return
		
	
	pass


class ruleFile(object):
	

	


	
	def __init__(self):
		# some constants
		self.NOERROR = 0
		self.ERRORSAVEFILE = 1
		self.ERRORSAVEFILE_NOBYTES = 2
		
		self.err = self.NOERROR
		self.theFile = globalvars.DATFILE
		self.editedByParser = False
		
		self.allowedKeys = [
			'Series',
			'Volume',
			'Imprint',
			'Publisher',
			'Number',
			'FileDirectory',
			'SeriesGroup',
			'Month',
			'Year',
			'MainCharacterOrTeam',
			'Format',
			'AlternateSeries',
			'Count',
			'FilePath',
			'FileName',
			'Genre',
			'Tags',
			'PageCount'
			]
			
		self.numericalKeys = [
			'Volume',
			'Month',
			'Year',
			'Count',
			'PageCount'
			]

		self.allowedKeyModifiers = [
			'Is',
			'Range',
			'Not',
			'Contains',
			'Greater',
			'GreaterEq',
			'Less',
			'LessEq',
			'Startswith',
			'StartsWithAnyOf',
			'ContainsAnyOf',
			'NotContainsAnyOf',
			'NotContains',
			'ContainsAllOf'
		]
		
		self.allowedKeyModifiersNumeric = [
			'Is',
			'Range',
			'Not',
			'Greater',
			'GreaterEq',
			'Less',
			'LessEq',
		]
		
	
			
		self.multiValueKeys = [
			'Tags',
			'Genre'
			]
			
		self.allowedVals = [
			'Series',
			'Volume',
			'Imprint',
			'Publisher',
			'Number',
			'SeriesGroup',
			'MainCharacterOrTeam',
			'Format',
			'AlternateSeries',
			'Count',
			'Genre',
			'Tags'
			]
			
		self.allowedValModifiers = [
			'SetValue',
			'Calc'
			]
			
		self.allowedValModifiersMulti = [
			'SetValue',
			'Add',
			'Replace',
			'Remove'
			]	
	
	def read(self):
		'''
		reading rules configuration
		returns string of parsed rules delimited by System.Environment.NewLine
		if the parser made any alterations the editedByParser property will be
		set to True
		'''
		s1=[]
		s = []
		myParser = parser()
		self.editedByParser = False
		if File.Exists(self.theFile):
			File.Copy(self.theFile, globalvars.BAKFILE, True) # just in case something bad happens
			s1 = File.ReadAllLines(self.theFile)
			s1 = [line for line in s1 if str.Trim(line) <> '']
			for line in s1:
				myParser.validate(str(line))
				if myParser.err:
					self.editedByParser = True
					pre = myParser.commentedLine(line)
				else:
					pre = line
				s.Add(pre)
		elif File.Exists(globalvars.SAMPLEFILE):
			s = File.ReadAllLines(globalvars.SAMPLEFILE)
				
		tmp = str('')
		s = [line for line in s if str.Trim(line) <> '']
		for line in s:
			tmp += '%s%s' % (line, System.Environment.NewLine)
		return tmp
	
	def write(self, theText):
		'''
		writes the context of the configurator window to a file
		returns ERROR constant (NOERROR if successful)
		if the parser made any alterations the editedByParser property will be
		set to True
		'''
		self.editedByParser = False
		s = str.split(str(theText),'\n')
		tmp = str('')
		errlines = 0
		myParser = parser()
		pre = ''
		
		s = [line for line in s if str.Trim(line) <> '']
	
		for line in s:
			myParser.validate(str(line))
			if myParser.err:
				pre = myParser.commentedLine(line)
				errlines += 1
				self.editedByParser = True
			else:
				pre = str(line)
			tmp += '%s%s' % (pre, System.Environment.NewLine)
		if len(tmp) > 0:
			try:
				File.WriteAllText(self.theFile, tmp)
			except Exception, err:
				return self.ERRORSAVEFILE
		else:
			return self.ERRORSAVEFILE_NOBYTES
	
		if not File.Exists(globalvars.CHKFILE):
			File.Create(globalvars.CHKFILE)
			
		return self.NOERROR
	
	def getAllowedKeyModifiers(self,myKey):
		myKey = str.lower(myKey)
		try:
			myModifierList = ['']
			if myKey == 'number' or myKey in [str.lower(x) for x in self.numericalKeys]:
				return self.allowedKeyModifiersNumeric
			if myKey not in [str.lower(x) for x in self.numericalKeys]:
				return self.allowedKeyModifiers
			return myModifierList
		except Exception, err:
			print str(err)	

	def getAllowedValModifiers(self,myKey):
		myKey = str.lower(myKey)
		try:
			myModifierList = ['']
			if myKey in [str.lower(x) for x in self.multiValueKeys]:
				return self.allowedValModifiersMulti
			else:
				return self.allowedValModifiers
		except Exception, err:
			print str(err)
		return ''
	
def readFile(theFile):
	if File.Exists(theFile):
		s = File.ReadAllLines(theFile)
	else:
		return str('')

	tmp = str('')
	s = [line for line in s if str.Trim(line) <> '']
	for line in s:
		tmp += '%s%s' % (line, System.Environment.NewLine)
	if len(s) == 0 and theFile == globalvars.LOGFILE:
		tmp = 'Your criteria matched no book. No data was touched by the Data Manager.'
	return tmp
