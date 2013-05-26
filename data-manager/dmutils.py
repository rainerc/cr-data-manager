# the utils module

import System
from System import String
from System.IO import File

#from System.Windows.Forms import MessageBox
import clr
import re
import globalvars

#clr.AddReference("ComicRack.Engine")
#from cYo.Projects.ComicRack.Engine import YesNo

class customFields:
	
	def __init__(self):
		self.theKey = ''
		self.theModifier = ''
		self.theVal = ''
		
	def parseRule(self,theRule):
		try:
			theRule = theRule.replace('<<','')
			theRule = theRule.replace('>>','')
			tmp = theRule.split(')',1)			# this will return 'Custom(MyHero','.Is:Batman'
			self.theKey = tmp[0] + ')'				# this is 'Custom(Hero'
			tmp2 = tmp[1].split(':')			# this is '.Is','Batman'
			self.theModifier = tmp2[0][1:]		# this is 'Is'
			if self.theModifier == '': self.theModifier = 'Is'			
			self.theVal = tmp2[1]				# this is 'Batman'
		except Exception, err:
			print str(err)	

	def parseAction(self,theRule):
		try:
			theRule = theRule.replace('<<','')
			theRule = theRule.replace('>>','')
			tmp = theRule.split(')',1)			# this will return 'Custom(MyHero','.Is:Batman'
			self.theKey = tmp[0] + ')'				# this is 'Custom(Hero'
			tmp2 = tmp[1].split(':')			# this is '.Is','Batman'
			self.theModifier = tmp2[0][1:]		# this is 'Is'
			if self.theModifier == '': self.theModifier = 'SetValue'			
			self.theVal = tmp2[1]				# this is 'Batman'
		except Exception, err:
			print str(err)	

	def customFieldName(self, myString):
		# get the field name of Custom(myField)
		myString = myString.replace('Custom(','')
		myString = myString.replace(')','')
		return myString


				
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
				s = str.split(unicode(line),'=')
				if str.Trim(s[0]) == myKey:
					return str.Trim(s[1])
		return ''

class comparer(object):
	"""description of class"""
	
	def __init__(self):
		clr.AddReference("ComicRack.Engine")
		from cYo.Projects.ComicRack.Engine import MangaYesNo, YesNo
		self.myYesNo = YesNo
		self.myMangaYesNo = MangaYesNo

	def yesNo(self,myString,myVal):
		myVal = myVal.lower()
		if myVal == 'yes': return myString == self.myYesNo.Yes
		elif myVal == 'no': return myString == self.myYesNo.No
		elif myVal == 'unknown' : return myString == self.myYesNo.Unknown
		elif myVal == '' : return myString == self.myYesNo.Unknown
		else : return False
		
	def mangaYesNo(self,myString,myVal):
		myVal = myVal.lower()
		if myVal == 'yes': return myString == self.myMangaYesNo.Yes
		elif myVal == 'no': return myString == self.myMangaYesNo.No
		elif myVal == 'unknown' : return myString == self.myMangaYesNo.Unknown
		elif myVal == '' : return myString == self.myMangaYesNo.Unknown
		elif myVal == 'yesandrighttoleft' : return myString == self.myMangaYesNo.YesAndRightToLeft
		else : return False
		
	
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

	def isAnyOf(self,myString,myVals,caseInsensitive):
		# example <<myString.IsAnyOf:val1,val2,val3>> 
		# or: <<Batman.IsAnyOf:Batman,Robin,Joker>>
		myString = unicode(myString).strip()
		myString = myString.strip()
		myVals = unicode(myVals)
		if caseInsensitive:
			myVals = myVals.lower()
			myString = myString.lower()
		theVals = myVals.strip(',').split(',')

		for word in theVals:
			if word.strip() == myString: return True
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
		myString = unicode(myString)
		myVal = unicode(myVal)
		if caseInsensitive == True:
			myString = myString.lower()
			myVal = myVal.lower()
		ret = myString.strip() == myVal.strip()
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
#	if String.Trim(str(s)) == '': return 0
	try:
		s = str(s).strip()
	except Exception, err:
		pass
	if s == '' : 
		return 0
	return s

def ireplace(text, old, new):
	# replaces after comparing case insensitive
	# replaces all occurences of [old] with [new]
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(old)
    return text

	
class multiValue(object):
	
	def __init__(self):
		theIni = iniFile(globalvars.USERINI)
		self.dateTimeFormat = theIni.read('DateTimeFormat')
		self.myParser = parser()
	
	def add(self,myField,myVals,book):
		'''
		add value or multiple values to a multi value field
		myField: content of field (like book.Tags)
		myVals: comma seperated list of values that shall be added
		returns: myField
		'''
#		myParser = parser()
		theVals = myVals.split(',')				# create list from myVals
		theList = myField.lower()				# create temp string from myField with all lower chars
		theList = theList.replace(' ,',',')		# eliminate blanks before and after comma in temp string
		theList = theList.replace(', ',',')
		myList = theList.split(',')				# create list from temp string
		for v in theVals:						# run through every value in theVals
			if v.lower().strip() not in myList and v <> '':		# if value not in temp list
				# old:
				# if v.startswith('book.'):
				if v.startswith('{'):
					v = self.myParser.parseCalc(v,str)
					print 'v: %s' % v
					print 'v eval: %s' %eval(v)
					myField += ',%s' % eval(v) 
				else:
					myField += ',%s' % v			# ... then add value to myField
				
		myField = myField.strip(',')
		return myField

	def replace(self, myList, oldVal, myVal, book):	# , caseinsensitive = True):
#		myParser = parser()
		oldVal = String.Trim(str(oldVal))
		myVal = String.Trim(str(myVal))
		newList = []
		theList = myList.strip(',').split(',')
		if oldVal.startswith('{'):
			oldVal = eval(self.myParser.parseCalc(oldVal,str))
		if myVal.startswith('{'):
			myVal = eval(self.myParser.parseCalc(myVal,str))
		for l in theList:			# iterate through every value of the old list
			l = String.Trim(l)
			# if caseinsensitive == True:
			if l.lower() == oldVal.lower(): l = myVal
			if newList.count(l) == 0:
				newList.Add(l)
		return ','.join(newList)
	
	def remove(self, myField, myVals, book):  # , caseinsensitive = True):
		'''
		remove value or multiple values from a multi value field
		myField: content of field (like book.Tags)
		myVals: comma seperated list of values that shall be removed
		returns: cleaned myField
		'''	
		theVals = myVals.split(',')				# create list from myVals
		myList = myField.split(',')				# create list from temp string
		print 'myList: %s' % myList
		tmpField = []
		for l in myList:
			for v in theVals:
				if v.startswith('{'): v = eval(self.myParser.parseCalc(v,str))
				if v.lower().strip() == l.lower().strip():
					l = ''
					break
			tmpField.Add(l)
		cleanedList = ','.join(tmpField)
		while ',,' in cleanedList:				# check for double commas
			cleanedList = cleanedList.replace(',,',',')
		cleanedList = cleanedList.strip(',').strip()	# check for leading or trailing blanks and commas
		return cleanedList

	
class dmString(object):
	def __init__(self):
		clr.AddReference("ComicRack.Engine")
		from cYo.Projects.ComicRack.Engine import MangaYesNo, YesNo
		from System import DateTime
#		theIni = iniFile(globalvars.USERINI)
#		self.dateTimeFormat = theIni.read('DateTimeFormat')	
		self.myYesNo = YesNo
		self.myMangaYesNo = MangaYesNo
		theIni = iniFile(globalvars.USERINI)
		self.dateTimeFormat = theIni.read('DateTimeFormat')
		self.myParser = parser()
	
	def yesNo(self,myVal):
		print 'dmString.yesno entered'
		myVal = myVal.lower()
		if myVal == 'yes': 
			print 'value is yes'
			print 'value: %s' % str(self.myYesNo.Yes)
			return self.myYesNo.Yes
		elif myVal == 'no': return self.myYesNo.No
		elif myVal == 'unknown': return self.myYesNo.Unknown
		elif myVal == '': return self.myYesNo.Unknown
		pass
	
	def mangaYesNo(self,myVal):
		myVal = myVal.lower()
		if myVal == 'yes': return self.myMangaYesNo.Yes
		elif myVal == 'no': return self.myMangaYesNo.No
		elif myVal == 'unknown': return self.myMangaYesNo.Unknown
		elif myVal == 'yesandlefttoright' : return self.myMangaYesNo.YesAndLeftToRight
		elif myVal == '': return self.myMangaYesNo.Unknown
		pass
	
	def toFloat(self, myVal):
		# tries to convert a string myVal to float
		# returns None if not possible or string myVal is empty
	
		print 'myVal @ toFloat: %s' % myVal
		try:
			return float(myVal)
		except Exception, err:
			pass
	
		s = myVal
	
		try:
			s = str(myVal).lower().strip()
			if s == '': return None
		except Exception, err:
			pass
		
		s = s.replace(chr(188),'.25')
		s = s.replace(chr(189),'.5')
		s = s.replace(u'\u221e','9999999')			# infinite symbol (∞)
	
		if s.startswith('minus'): s = s.replace('minus','-')
	
		try:
			return float(s)
		except Exception, err:
			tmp = ''
			for c in s:
				if c in ('.','-') or c.isdigit():
					tmp += c
				else:
					break
			try:
				return float(tmp)
			except Exception, err:
				return None
			
	def add(self, myKey, myVal, book):
#		myParser = parser()
		if myVal.startswith('{'):
			myVal = self.myParser.parseCalc(myVal,str)
			print 'v: %s' % myVal
			print 'v eval: %s' %eval(myVal)
			return str(myKey) + eval(myVal) 
		else:
			return str(myKey) + str(myVal)
		pass
	
	def replace(self, myKey,oldVal,newVal,book): # caseinsensitive = True):
#		myParser = parser()
		if oldVal.startswith('{'): oldVal = eval(self.myParser.parseCalc(oldVal,str))
		if newVal.startswith('{'): newVal = eval(self.myParser.parseCalc(newVal,str))
		print 'oldVal: %s ' % oldVal	
		print 'newVal: %s ' % newVal
		# if caseinsensitive == True:
		return ireplace(myKey, oldVal, newVal).lstrip()
#		else:
#			return myKey.replace(oldVal,newVal)
		pass
	
	def remove(self, myKey,myVal, book):  # caseinsensitive = True):
		if myVal.startswith('{'): myVal = eval(self.myParser.parseCalc(myVal,str))
#		if caseinsensitive == True:
		return ireplace(myKey,myVal,'').lstrip()
#		else:
#			return myKey.replace(myVal,'').lstrip()
		pass
	
	def removeLeading(self, myKey,myVal, book): # caseinsensitive = True):
		#	myKey = myKey.strip()		# we must not strip here!
	#	leadsWith = False
		if myVal.startswith('{'): myVal = eval(self.myParser.parseCalc(myVal,str))
	#	if caseinsensitive == True and myKey.lower().startswith(myVal.lower()):
		if myKey.lower().startswith(myVal.lower()):
	#		leadsWith = True
	#	elif myKey.startswith(myVal):
	#		leadsWith = True
	#	if leadsWith == True:
			return myKey[len(myVal):].lstrip()
		else:
			return myKey
		
	def setValue(self,myVal,book):
		if myVal.startswith('{'): myVal = eval(self.myParser.parseCalc(myVal,str))
		return myVal

class dmDateTime(object):

	def __init__(self):
		self.myParser = parser()
		pass
	
	def setValue(self,myKey,myVal,book):
		print 'myVal: %s' % myVal
		if myVal.startswith('{'): 
			myVal = eval(self.myParser.parseCalc(myVal,DateTime))
		elif myVal == '': 
			myVal = System.DateTime.MinValue
		else: 
			myVal = System.DateTime.Parse(myVal)
		return myVal

class dmNumeric(object):
	def __init__(self):
		self.myParser = parser()
		self.dmString = dmString()
		pass
	
	def setValue(self,myKey,myVal,book):
		if str(myVal).startswith('{'): 
			# no other way to pass a Null value from a field variable:
			tmpVal = myVal.strip('{').strip('}')
			if eval('book.%s' % tmpVal) == '':
				return -1
			else:
				myVal = eval(self.myParser.parseCalc(myVal,int))
				print 'myVal: %s' % myVal
		elif str(myVal).strip() == '':
			myVal = -1
		else:
			return myVal
		return myVal

class dmYesNo(object):
	def __init__(self):
		print 'YesNo entered'
		clr.AddReference("ComicRack.Engine")
		from cYo.Projects.ComicRack.Engine import YesNo
		self.myParser = parser()
		self.dmString = dmString()
		
	def setValue(self,myKey,myVal,book):
		print 'setValue entered'
		print 'myVal: %s' % myVal
		if str(myVal).startswith('{'):
			myVal = eval(self.myParser.parseCalc(myVal,YesNo))
		else:
			print 'myVal @ dm.setValue'
			myVal = self.dmString.yesNo('%s' % myVal)
		return myVal
		
class parser(object):
	
	def __init__(self):
		print 'parser entered'
		self.err = False
		self.error = ''
		clr.AddReference("ComicRack.Engine")
		from cYo.Projects.ComicRack.Engine import YesNo
		self.YesNo = YesNo
		
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
		
		return
		
	def getField(self,myField):
		'''
		converts {Series} to 'book.Series'
		'''
		myField = myField.replace('{','book.')
		myField = myField.replace('}','')
		return myField
	
	def castType(self,myField,myType):
		'''
		returns a typeCaster
		example: parser.castType('{Series}',str)
		returns: 'unicode(book.Series)'
		'''
		myRules = ruleFile()
		myField = self.getField(myField)
		myField = myField.replace('book.','')
		
		print 'CastType entered'
		
		if myType == str:
			if myField in myRules.dateTimeKeys:
				# return 'dmString.dateTimeToString(book.%s)' % myField
				return 'book.%s.ToString(self.dateTimeFormat)' % myField
			else:
				return 'unicode(book.%s)' % myField
			
		elif myType == int:
			return 'int(self.dmString.toFloat(book.%s))' % myField

#			return 'self.dmString.toFloat(book.%s)' % myField
		
		elif myType == DateTime:
			return 'System.DateTime.Parse(book.%s)' % myField
			
		elif myType == self.YesNo:
			print 'CastType trying'
			return 'self.dmString.YesNo(book.%s)' % myField
		
		pass
	
	def parseCalc(self,theString,theType):
		'''
		parses the Calc modifier depending on the field type
		example: parser.parseCalc({Series} + 'Hugo', str)
		returns: 'unicode(book.Series) + 'Hugo''
		'''
		
		print 'theType @ parseCalc %s' % str(theType)
		while '{' in theString:
			m = re.search('{.*?}',theString)
			tmpField = m.group(0)				# returns {series}, e.g.
			myExpression = self.castType(tmpField,theType) # now we want to change {Series} to unicode(book.Series)
			theString = theString.replace(tmpField,myExpression)
			
		print 'theString: %s' % theString
		return theString
	
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
		self.yesNoKeys = myIni.read('yesNoKeys').split(',')
		self.mangaYesNoKeys = myIni.read('mangaYesNoKeys').split(',')
		self.dateTimeKeys = myIni.read('dateTimeKeys').split(',')
		self.allowedKeyModifiers = myIni.read('allowedKeyModifiers').split(',')
		self.allowedKeyModifiersNumeric = myIni.read('allowedKeyModifiersNumeric').split(',')
		self.allowedKeyModifiersMulti = myIni.read('allowedKeyModifiersMulti').split(',')
		self.languageISOKeys = myIni.read('languageISOKeys').split(',')
		
		# allowed keys and modifiers for left part of rule
		self.allowedVals = myIni.read('allowedVals').split(',')
		#self.allowedValsMulti = myIni.read('allowedValsMulti').split(',')
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
				myParser.validate(unicode(line))
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
		theText = unicode(theText)
		s = String.Split(theText,'\n')
		# s = str.split(str(theText),'\n')
		tmp = str('')
		errlines = 0
		myParser = parser()
		pre = ''
		
		s = [line for line in s if str.Trim(line) <> '']
	
		for line in s:
			myParser.validate(unicode(line))
			if myParser.err:
				pre = myParser.commentedLine(line)
				errlines += 1
				self.editedByParser = True
			else:
				pre = unicode(line)
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
