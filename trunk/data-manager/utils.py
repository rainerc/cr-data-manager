# the utils module

import System
from System import String
from System.IO import File

#from System.Windows.Forms import MessageBox
import re
import globalvars

class iniFile:
	def __init__(self,theFile = globalvars.INIFILE):
		self.theFile = theFile
		pass
	
	def write(self, myKey, myVal):
		'''
		writes the key myKey and value myVal to the ini-file
		
		ini file is build like this:
			myKey = myValue
		
		if the file does not exist the first call of method write creates it
			
		'''

		if File.Exists(self.theFile):
			linefound = False
			newConfig = []
			myLines = File.ReadAllLines(self.theFile)
			for line in myLines:
				s = str.split(line,'=')
				if str.lower(str.Trim(s[0])) == str.lower(myKey):
					line = '%s = %s' % (myKey, myVal)
					linefound = True
				newConfig.append(line)
			if linefound == False:
				newConfig.append('%s = %s' % (myKey, myVal))
			File.WriteAllLines(self.theFile,newConfig)
		else:
			File.AppendAllText(self.theFile,'%s = %s%s' % (myKey, myVal, System.Environment.NewLine))
		return
	
	
	def read(self, myKey):
		'''
		retrieves the value of myKey in Ini-file theFile
		returns '' if key myKey was not found
		'''
		if File.Exists(self.theFile):
			myLines = File.ReadAllLines(self.theFile)
			for line in myLines:
				s = str.split(line,'=')
				if str.Trim(s[0]) == myKey:
					return str.Trim(s[1])
		return ''

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

	def startsWithAnyOf(self, myString, myVals, caseInsensitive):
		myString = myString.strip()
		theVals = myVals.strip(',').split(',')
		for word in theVals:
			if caseInsensitive == True:
				if myString.lower().StartsWith(word.strip().lower()):
					return True
			else:
				if myString.StartsWith(word.strip()):
					return True
		return False


	def containsAnyOf(self, myString, myVals,caseInsensitive):
		# example <<myString.containsAnyOf:val1,val2,val3>> 
		# or: <<The Adventures of Batman.ContainsAnyOf:Batman,Robin,Joker>>

		myString = myString.strip()
		if caseInsensitive:
			myVals = myVals.lower()
			myString = myString.lower()
		theVals = myVals.strip(',').split(',')
	
		for word in theVals:
			if word.strip() in myString: return True
		return False

	# todo: this is redundant
	def notContainsAnyOf(self, myString,myVals,caseInsensitive):
		myString = myString.strip()
		if caseInsensitive:
			myVals = myVals.lower()
			myString = myString.lower()
		theVals = myVals.strip(',').split(',')

		for word in theVals:
			if word.strip() in myString: return False
		return True

	def containsAllOf(self, myString, myVals,caseInsensitive):
		# example <<myString.containsAllOf:val1,val2,val3>> 
		# or: <<The Adventures of Batman.ContainsAllOf:Batman,Robin,Joker>>

		myString = myString.strip()
		if caseInsensitive:
			myVals = myVals.lower()
			myString = myString.lower()
		theVals = myVals.strip(',').split(',')
		
		for word in theVals:
			if not word.strip() in myString: return False
		return True			

	def contains(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myVal.strip() in myString

	
	# todo: this is redundant
	def containsNot(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)	
		return myVal.strip() not in myString			
	
	def equals(self, myString, myVal, caseInsensitive):

		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString.strip() == myVal.strip()

	def startsWith(self, myString, myVal, caseInsensitive):
		if caseInsensitive == True:
			myString = str.lower(myString)
			myVal = str.lower(myVal)
		return myString.startswith(myVal.strip())
	
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
	if String.Trim(str(s)) == '': return 0
	return s


def stringAdd(myKey, myVal):
	return str(myKey) + str(myVal)

def stringReplace(myKey,oldVal,newVal):
	return myKey.replace(oldVal,newVal)

def stringRemove(myKey,myVal):
	return myKey.replace(myVal,'')

def stringRemoveLeading(myKey,myVal):
#	myKey = myKey.strip()
	if myKey.startswith(myVal):
		myKey = myKey.replace(myVal,'',1)
	return myKey
		
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
		
		myIni = iniFile()
		
		# allowed keys and modifiers for left part of rule
		self.allowedKeys = myIni.read('allowedKeys').split(',')
		self.numericalKeys = myIni.read('numericalKeys').split(',')
		self.pseudoNumericalKeys = myIni.read('pseudoNumericalKeys').split(',')
		self.multiValueKeys = myIni.read('multiValueKeys').split(',')
		self.allowedKeyModifiers = myIni.read('allowedKeyModifiers').split(',')
		self.allowedKeyModifiersNumeric = myIni.read('allowedKeyModifiersNumeric').split(',')
		self.allowedKeyModifiersMulti = myIni.read('allowedKeyModifiersMulti').split(',')
		
		# allowed keys and modifiers for left part of rule
		self.allowedVals = myIni.read('allowedVals').split(',')
		self.allowedValsMulti = myIni.read('allowedValsMulti').split(',')
		self.allowedValModifiers = myIni.read('allowedValModifiers').split(',')
		self.allowedValModifiersMulti = myIni.read('allowedValModifiersMulti').split(',')
		
		# -------------------------------------------------------------------------------------------
		# todo: not sure if this is necessary
		self.allowedValsNumeric = [				# every allowed numeric key in right part of rule
			'Volume',
			'Number',
			'Count',
			'AlternateNumber',
			'AlternateCount',
			]
			
		self.allowedValModifiersNumeric = [
			'SetValue',
			'Calc'
			]
		# -------------------------------------------------------------------------------------------
	

	def dummy():

		self.allowedValModifiersMulti = [		# every allowed modifier for multi-value fields in right part of rule
			'SetValue',
			'Add',
			'Replace',
			'Remove'
			]	
					
		self.allowedValModifiers = [			# every allowed modifier in right part of rule
			'SetValue',
			'Calc',
			'Add',
			'Remove',
			'Replace',
			'RemoveLeading'
			]
	
		self.allowedValsMulti = [				# every allowed multi-value key in right part of rule
			'Tags',
			'Genre'
			]
		self.allowedVals = [
			'AgeRating', #ATTN:docdoom Added String Key
            'AlternateCount',
			'AlternateSeries',
			'AlternateNumber',
			'BookNotes', #ATTN:docdoom Added String Key
            'BookOwner', #ATTN:docdoom Added String Key
			'BookStore', #ATTN:docdoom Added String Key
            'Characters', #ATTN:docdoom Added Multi-value Key
            'Colorist', #ATTN:docdoom Added Multi-value Key
            'Count',
			'CoverArtist', #ATTN:docdoom Added Multi-value Key
            'Day',#ATTN:docdoom Added Numeric Key
            'Editor', #ATTN:docdoom Added Multi-value Key
            'Format',
			'Genre',
			'Imprint',
			'Inker', #ATTN:docdoom Added Multi-value Key (also included in multi-value below it was the only missing one)
            'ISBN', #ATTN:docdoom Added String Key
            'Letterer', #ATTN:docdoom Added Multi-value Key
            'Locations', #ATTN:docdoom Added Multi-value Key
			'MainCharacterOrTeam',
			'Month',
			'Notes', #ATTN:docdoom Added String Key
            'Number',
			'PageCount',
			'Penciller', #ATTN:docdoom Added Multi-value Key
            'Publisher',
			'Review', #ATTN:docdoom Added String Key
            'ScanInformation', #ATTN:docdoom Added String Key
            'Series',
			'SeriesGroup',
			'StoryArc', #ATTN:docdoom Added String Key
            'Summary', #ATTN:docdoom Added String Key
            'Tags',
			'Teams', #ATTN:docdoom Added Multi-value Key
            'Title',
            'Volume',
			'Web', #ATTN:docdoom Added String Key
            'Writer', #ATTN:docdoom Added Multi-value Key
            'Year'
			]

		self.allowedKeyModifiersMulti = [		# every allowed modifier for multi-value fields in left part of rule
			'Is',
			'Not',
			'Contains',
			'ContainsAnyOf',
			'NotContainsAnyOf',
			'NotContains',
			'ContainsAllOf'
		]
	
		self.allowedKeyModifiersNumeric = [		# every allowed modifier for numeric fields in left part of rule
			'Is',
			'Range',
			'Not',
			'Greater',
			'GreaterEq',
			'Less',
			'LessEq',
		]

		self.allowedKeyModifiers = [	# every allowed modifier in left part of rule
			'Is',
			'Not',
			'Contains',
			'Greater',
			'GreaterEq',
			'Less',
			'LessEq',
			'StartsWith',
			'NotStartsWith',
			'StartsWithAnyOf',
			'NotStartsWithAnyOf',
			'ContainsAnyOf',
			'NotContainsAnyOf',
			'NotContains',
			'ContainsAllOf'
		]
		
		self.multiValueKeys = [
			'Characters',
            'Colorist',
            'CoverArtist',
            'Editor',
            'Genre',
            'Inker', #ATTN:docdoom added (Seems you already had most all these added even if not referenced in Allowed keys)
			'Letterer',
            'Locations',
            'Penciller',
            'Tags',
			'Teams',
            'Writer',
            ]

#		self.pseudoNumericalKeys = [	# every allowed pseudo-numerical key to be used in left part of rule
#			'Number',
#			'AlternateNumber'
#			]


#		allowedKeys = [		 # every allowed key to be used in left part of rule
#			'AgeRating',
#			'AlternateNumber',
#			'AlternateCount',
#			'Series',
#			'Volume',
#			'Imprint',
#			'Publisher',
#			'Number',
#			'FileDirectory',
#			'SeriesGroup',
#			'Month',
#			'Year',
#			'MainCharacterOrTeam',
#			'Format',
#			'AlternateSeries',
#			'Count',
#			'FilePath',
#			'FileName',
#			'Genre',
#			'Tags',
#			'PageCount',
#			'Title'
#			]
#						#		self.allowedKeys = [
#			#			'AgeRating', #ATTN:docdoom Added String Key
#			#            'AlternateCount',
#			#			'AlternateSeries',
#			#			'AlternateNumber',
#			#			'BookNotes', #ATTN:docdoom Added String Key
#			#            'BookOwner', #ATTN:docdoom Added String Key
#			#			'BookStore', #ATTN:docdoom Added String Key
#			#            'Characters', #ATTN:docdoom Added Multi-value Key
#			#            'Colorist', #ATTN:docdoom Added Multi-value Key
#			#            'Count',
#			#			'CoverArtist', #ATTN:docdoom Added Multi-value Key
#			#            'Day', #ATTN:docdoom Added Numeric Key
#			#            'Editor', #ATTN:docdoom Added Multi-value Key
#			#            'FileDirectory',
#			#			'FileFormat',  #ATTN:docdoom Added String Key (Read-Only so not valid for values)
#			#            'FileName',
#			#			'FilePath',
#			#			'Format',
#			#			'Genre',
#			#			'Imprint',
#			#			'Inker', #ATTN:docdoom Added Multi-value Key (also included in multi-value below it was the only missing one)
#			#            'ISBN', #ATTN:docdoom Added String Key
#			#            'Letterer', #ATTN:docdoom Added Multi-value Key
#			#            'Locations', #ATTN:docdoom Added Multi-value Key
#			#			'MainCharacterOrTeam',
#			#			'Month',
#			#			'Notes', #ATTN:docdoom Added String Key
#			#            'Number',
#			#			'PageCount',
#			#			'Penciller', #ATTN:docdoom Added Multi-value Key
#			#            'Publisher',
#			#			'Review', #ATTN:docdoom Added String Key
#			#            'ScanInformation', #ATTN:docdoom Added String Key
#			#            'Series',
#			#			'SeriesGroup',
#			#			'StoryArc', #ATTN:docdoom Added String Key
#			#            'Summary', #ATTN:docdoom Added String Key
#			#            'Tags',
#			#			'Teams', #ATTN:docdoom Added Multi-value Key
#			#            'Title',
#			#            'Volume',
#			#			'Web', #ATTN:docdoom Added String Key
#			#            'Writer', #ATTN:docdoom Added Multi-value Key
#			#            'Year'
#			#            ]
#
#		self.numericalKeys = [
#				'AlternateCount',
#				'Count',
#				'Day', #ATTN:docdoom -added here and above
#	            'Month',
#				'PageCount',
#				'Volume',
#				'Year'
#				]
#		return
		pass
	


	
	def groupHeaders(self, theFile = globalvars.DATFILE):
		'''
		returns a list of group headers in the rule set
		'''
		headers = []
		if File.Exists(theFile):
			s1 = File.ReadAllLines(theFile)
			s1 = [line for line in s1 if String.StartsWith(line, '#@ GROUP')]
			for line in s1:
				headers.Add(String.Replace(line,'#@ GROUP ',''))
							
		return headers
	
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
			if myKey == 'number' or myKey == 'alternatenumber' or myKey in [str.lower(x) for x in self.numericalKeys]:
				return self.allowedKeyModifiersNumeric
			if myKey in [str.lower(x) for x in self.multiValueKeys]:
				return self.allowedKeyModifiersMulti
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
