'''
how to use:
For every book:
1. in dmProgressForm call dmparser.matchAllRules(ruleset,book)
2.		matchAllRules first initializes all variables
2.		matchAllRules calls AnalyzeRuleSet which sets the values of dmParser.actions and dmParser.rules
3.		matchAllRules calls matchRule for every rule in dmParser.rules
4.			matchRule calls AnalyzeRule which sets dmParser.theRuleKey, dmParser.theRuleModifier and dmParser.theRuleVals (via CastType)
4. if matchAllRules returns True:
5. make a copy of the original book to store the original field contents (book.Clone())
5. in dmProgressForm call dmparser.executeAllActions(book)
6.		executeAllActions calls executeAction for every action in dmParser.actions, sets dmparser.FieldsTouched to None
7.		executeAction calls AnalyzeAction to set dmParser.theActionKey, dmParser.theActionModifier, dmParser.theActionValue
8.		executeAction appends the field currently in use to dmparser.FieldsTouched
9.		executeAction finally executes the action


calc works like this:
1. executAction calc
2. castType


'''

import System
import clr
import re
clr.AddReference("ComicRack.Engine")
from cYo.Projects.ComicRack.Engine import YesNo, MangaYesNo

import globalvars
import dmutils
from dmutils import customFields
customField = customFields()
from dmutils import ruleFile, iniFile, dmString, comparer, multiValue
dmString = dmString()
comparer = comparer()
multiValue = multiValue()
dataManIni = iniFile(globalvars.INIFILE)
userIni = iniFile(globalvars.USERINI)

class dmParser(object):
	
	def __init__(self):
		self.initializeVars()
		self.ruleFile = ruleFile()
		

	def initializeVars(self):
		self.error = False
		self.errCount = 0
		self.rules = []
		self.actions = []
		self.theRuleKey = ''
		# later on replace this:
		#self.theRuleValue = ''
		# with this:
		self.theRuleValues = []
		self.theRuleModifier = ''
		self.theActionKey = ''
		self.theActionValue = []
		self.theActionModifier = ''
		self.fieldsTouched = []
		self.listDelimiter = dataManIni.read("ListDelimiter")
		self.theLog = ''
		self.ruleMode = 'AND'
		self.dateTimeFormat = userIni.read('DateTimeFormat')

			
		
	# TODO: do we really need this stuff anymore?
	def getField(self,myField):
		'''
		converts {Series} to 'book.Series'
		'''
		myField = myField.replace('{','book.')
		myField = myField.replace('}','')
		return myField
	
	def fieldValue(self, theString, book):
		'''
		returns the value of a field
		example: dmParser.fieldValue('Series') 
		returns: value of field books.Series
		'''
		if theString.startswith('Custom'):
			s = theString.split(')')
			cf = s[0].replace('Custom(','')
			return eval("book.GetCustomValue(\'%s\'" % cf )
		else:
			return eval('book.%s' % theString)
	# end TODO	


	def parseCalc(self,theField = '',theValue = '',book = object):
		allowedKeys = dataManIni.read('allowedKeys').split(',')
		while '{' in theValue:
			# retrieve each {field} in theField
			m = re.search('{.*?}',theValue)
			fieldName = m.group(0).lstrip('{').rstrip('}')
			if fieldName in allowedKeys:
				pass
				# get the value of {field} with getattr(book)
				fieldContent = getattr(book,fieldName)
				# we cannot use castType() here because it expects a list as parameter
				# so we use castTypeSingleValue()
				fieldContent = self.castTypeSingleValue(theField, unicode(fieldContent))
				if fieldName in self.ruleFile.dateTimeKeys:
					fieldContentToDateTime = System.DateTime.Parse(fieldContent)
					fieldContent = System.DateTime.ToString(fieldContentToDateTime,self.dateTimeFormat)
				if type(fieldContent) == str and theField not in ['Number','AlternateNumber']:
					fieldContent = fieldContent.replace('\n','\\n')
					fieldContent = '\'%s\'' % fieldContent
					pass
				newValue = theValue.replace('{' + fieldName + '}', unicode(fieldContent))
			else:
				newValue = theValue.replace('{' + fieldName + '}','<<<<' + fieldName + '>>>>')

			
			theValue = newValue
		theValue = theValue.replace('<<<<','{').replace('>>>>','}')
		try:
			print theValue
			# this throws an exception when used with regexReplace:
			return eval(theValue)
			# so we try this:
			#return eval('' + theValue)
		except Exception,err:
			#return theValue
			if self.theActionModifier.startswith('Reg'):
				return theValue
		except:
			print 'Exception: %s' % Exception.ToString
			self.error = True
			self.errCount += 1
			#print 'Err: %S' % err
			return ''
		
	def analyzeRuleSet(self, ruleLine):
		'''
		analyzes a complete rule set
		sets the values of dmParser.actions and dmParser.rules
		example: <<Series:Batman>><<Volume:2011>>
		'''
		if ruleLine.startswith('|'):
			self.ruleMode = 'OR'
			ruleLine = ruleLine.lstrip('|')
		ruleLine = ruleLine.replace('<<','')
		theParts = ruleLine.split('=>')
		theRules = theParts[0].split('>>')
		self.rules = []
		for rule in theRules:
			if rule.strip() <> '': self.rules.append(rule.strip()) 
		theActions = theParts[1].split('>>')
		for action in theActions:
			if action.strip() <> '': self.actions.append(action)
		return

	def analyzeRule(self, theRule):
		'''
		analyzes a single rule of a complete rule
		sets the values of dmParser.theRuleKey, dmParser.theRuleModifier and dmParser.theRuleValue
		example:
		dmParser.analyzeRule('Series.Is:Batman')
		dmParser.analyzeRule('Custom(myField).Is:myVal)
		sets:
		Key:Series	Modifier:Is	Value:Batman
		Key:Custom(myField)	Modifier:Is	Value:myVal
		'''
		
		myValue = ''
		if theRule.startswith('Custom'):
			customField.parseRule(theRule)
			self.theRuleKey = customField.theKey.strip()
			self.theRuleModifier = customField.theModifier.strip()
			# replace this:
			#self.theRuleValue = customField.theVal.strip()
			# with:
			self.theRuleValues.append(customField.theVal.strip())
		else:
			s = theRule.split(':',1)
			self.theRuleKey = s[0].strip()
			myValue = s[1].strip()
			if '.' in s[0]:
				self.theRuleKey = s[0].split('.')[0].strip()
				self.theRuleModifier = s[0].split('.')[1].strip()
			else:
				self.theRuleModifier = 'Is'
		if self.theRuleModifier in self.ruleFile.multipleParamKeyModifiers:
			# self.theRuleValues = myValue.split(',')
			self.theRuleValues = myValue.split(self.listDelimiter)
		else:
			self.theRuleValues.append(myValue)
		# NOTE: the rule values are written to list theRuleValues after casted to the right type
		self.theRuleValues = self.castType(self.theRuleKey,self.theRuleValues)
	
	def	analyzeAction(self, theAction,book):
		'''
		analyzes a single action 
		sets the values of dmParser.theActionKey, dmParser.theActionModifier and dmParser.theActionValue
		example:
		dmParser.analyzeAction('Series.SetValue:Batman')
		dmParser.analyzeRule('Custom(myField).SetValue:myVal)
		sets:
		Key:Series	Modifier:SetValue	Value:Batman
		Key:Custom(myField)	Modifier:SetValue	Value:myVal
		'''
		allowedKeys = dataManIni.read('allowedKeys').split(',')
		actionValues = []
		theActionValue = ''
		if theAction.strip().startswith('Custom'):
			customField.parseAction(theAction)
			self.theActionKey = customField.theKey.strip()
			self.theActionModifier = customField.theModifier.strip()
			theActionValue = customField.theVal.strip()
			#self.theActionValue.append(actionValues)
		else:
			s = theAction.split(':',1)
			self.theActionKey = s[0].strip()
			# do not use this:
			# actionValues = s[1].strip()
			theActionValue = s[1]
			if '.' in s[0]:
				self.theActionKey = s[0].split('.')[0].strip()
				self.theActionModifier = s[0].split('.')[1].strip()
			else:
				self.theActionModifier = 'SetValue'
			
		if self.theActionKey in self.ruleFile.multiValueKeys or self.theActionModifier in ['RegexReplace','Replace']:
			tmpList = theActionValue.split(self.listDelimiter)
			# tmpList = theActionValue.split(',')
			for v in tmpList:
				if v.startswith('{') and v.endswith('}') and v.count('{') == 1:
					tmpVal = v.replace('{','').replace('}','')
					if tmpVal in allowedKeys:
						v = getattr(book,tmpVal)
				if '{' in v:
					v = self.parseCalc(self.theActionKey,v,book)
				actionValues.append(v)
		elif '{' in theActionValue:
			if theActionValue.startswith('{') and theActionValue.endswith('}') and theActionValue.count('{') == 1:
					tmpVal = theActionValue.strip('{').strip('}')
					if tmpVal in allowedKeys:
						theActionValue = str(getattr(book,tmpVal))
			if '{' in theActionValue:
				theActionValue = self.parseCalc(self.theActionKey,theActionValue,book)
			actionValues.append(unicode(theActionValue))
		else:
			actionValues.append(theActionValue)

		# now cast all action values to the correct type
		if self.error == False:
			self.theActionValue = self.castType(self.theActionKey,actionValues)

	def matchRule(self, theRule, book):
		'''
		calls analyzeRule and then checks if the books matches to the rule
		'''
		self.analyzeRule(theRule)
		theKey = self.theRuleKey
		theModifier = self.theRuleModifier
		theValue = self.theRuleValues

		try:
			
			if theKey.startswith('Custom'):
				myCustomFieldName = customField.customFieldName(theKey)
				if theValue[0] == None: 
					theValue[0] = ''
				customValue = book.GetCustomValue(myCustomFieldName)
				if customValue == None:
					customValue = ''
				matched = customValue.lower().strip() == theValue[0].lower().strip()
				if theModifier == 'Is':
					return matched
				else:
					return not matched

			if theModifier == 'Is': return self.equals(theKey,theValue[0],book)	
			elif theModifier == 'Not': return not self.equals(theKey,theValue[0],book)	
			elif theModifier == 'Greater': return self.greater(theKey,theValue[0],book)
			elif theModifier == 'GreaterEq': return self.greaterEq(theKey,theValue[0],book)
			elif theModifier == 'Less': return self.less(theKey,theValue[0],book)
			elif theModifier == 'LessEq': return self.lessEq(theKey,theValue[0],book)
			elif theModifier == 'IsAnyOf': return self.isAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'NotIsAnyOf': return not self.isAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'StartsWith': return getattr(book, theKey).lower().startswith(theValue[0].lower())
			elif theModifier == 'NotStartsWith': return not getattr(book, theKey).startswith(theValue[0])
			elif theModifier == 'StartsWithAnyOf': return self.startsWithAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'NotStartsWithAnyOf': return not self.startsWithAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'RegEx': return comparer.regex(getattr(book,theKey),theValue[0])
			elif theModifier == 'NotRegEx': return not comparer.regex(getattr(book,theKey),theValue[0])
			elif theModifier == 'Contains': return comparer.contains(getattr(book,theKey),theValue[0])
			elif theModifier in ['NotContains','ContainsNot']: return not comparer.contains(getattr(book,theKey),theValue[0])
			elif theModifier == 'ContainsAnyOf': return self.containsAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'NotContainsAnyOf': return not self.containsAnyOf(getattr(book,theKey),theValue)
			elif theModifier == 'ContainsAllOf': return self.containsAllOf(getattr(book,theKey),theValue)		 
			elif theModifier == 'NotContainsAllOf': return not self.containsAllOf(getattr(book,theKey),theValue)		 
			elif theModifier == 'Range': return self.range(theKey,theValue,book)
			elif theModifier == 'NotRange': return not self.range(theKey,theValue,book)

		except Exception, err:
			print 'Err @ matchRule: %s' % str(err)
		return None

	def matchAllRules(self, theRules,book):
		'''
		checks if all rules in the ruleset match
		this has to be updated whence OR is implemented
		'''
		self.initializeVars()
		self.analyzeRuleSet(theRules)

		for rule in self.rules:
			self.theRuleValues = []
			matched = self.matchRule(rule,book)
			if self.ruleMode == 'OR' and matched == True:
				return True
			if self.ruleMode == 'AND' and not matched: return False
		if self.ruleMode == 'AND' :
			return True
		else :
			return False

	def castTypeSingleValue(self, theField, theValue=''):
		tmpList = []
		tmpList.append(theValue)
		return self.castType(theField,tmpList)[0]
		

	def castType(self, theField, theValue=[]):
		'''
		casts the type of each value in list theValue so that it fits to the type of the field
		'''
		try:
			tmpList = []
			for v in theValue:
				if v.strip() == '':
					if theField in self.ruleFile.numericalKeys: 
						v = '-1'
					elif theField in self.ruleFile.dateTimeKeys: 
						v = str(System.DateTime.MinValue)
				if theField in self.ruleFile.dateTimeKeys: tmpList.append(System.DateTime.Parse(v))
				elif theField in self.ruleFile.yesNoKeys: tmpList.append(dmString.yesNo(v))
				elif theField in self.ruleFile.mangaYesNoKeys: tmpList.append(dmString.mangaYesNo(v))
				elif theField in self.ruleFile.numericalKeys: tmpList.append(float(v))
				#elif theField in ['Number','AlternateNumber']: 
				#	v = self.toFloat(unicode(v))
				#	if v == None: v = ''
				#	tmpList.append(v)
				else: tmpList.append(unicode(v))
			return tmpList
		except Exception,err:
			print 'Err @ castType: %s' % str(err)
	
	def executeAction(self,theAction,book):
		self.error = False
		self.analyzeAction(theAction,book)
		if self.error == True:
			self.theLog  += '\t%s\n\tError in Action %s\n\t%s\n' % (40 * '*',theAction, 40 * '*')
			return
		theKey = self.theActionKey
		theModifier = self.theActionModifier
		theValue = self.theActionValue
		if theKey not in self.fieldsTouched:
			self.fieldsTouched.append(theKey)

		try:
			if theKey.startswith('Custom'):
				myCustomFieldName = customField.customFieldName(theKey)
				book.SetCustomValue(myCustomFieldName, theValue[0])
			elif theModifier == 'SetValue' or theModifier == 'Calc':
				if theKey in self.ruleFile.multiValueKeys:
					newVal = multiValue.setMulti(theKey, theValue)
					setattr(book,theKey,newVal)
				else:
					setattr(book,theKey,theValue[0])
			elif theModifier == 'Add':
				if theKey in self.ruleFile.multiValueKeys:
					newVal = multiValue.addMulti(getattr(book,theKey),theValue)
					setattr(book,theKey,newVal)
				else:
					setattr(book,theKey,getattr(book,theKey) + theValue[0])
			elif theModifier == 'Replace':
				if theKey in self.ruleFile.multiValueKeys:
					newVal = multiValue.replaceMulti(getattr(book,theKey),theValue)
				else:
					newVal = dmString.replaceString(getattr(book,theKey), theValue)
				setattr(book,theKey,newVal)
			elif theModifier == 'Remove':
				if theKey in self.ruleFile.multiValueKeys:
					newVal = multiValue.removeMulti(getattr(book,theKey), theValue)
				else:
					newVal = dmString.removeString(getattr(book,theKey), theValue[0])
				setattr(book,theKey,newVal)
			elif theModifier == 'RegexReplace':
				if theKey in self.ruleFile.multiValueKeys:
					pass		# has to be implemented yet
				else:
					newVal = dmString.regexReplace(getattr(book,theKey), theValue)
				setattr(book,theKey,newVal)
			elif theModifier == 'RemoveLeading':
				newVal = dmString.removeLeadingString(getattr(book,theKey), theValue[0])
				setattr(book,theKey,newVal)
			else:
				pass

		except Exception, err:
			print 'err @ executeAction: %s' % str(err)

	def executeAllActions(self,book):
		self.fieldsTouched = []

		for action in self.actions:
			self.theActionValue = []
			self.executeAction(action,book)
			if self.error == True and userIni.read("BreakAfterFirstError") == "True":
				return

	def equals(self,myKey,myVal,book):
		if type(myVal) == System.DateTime:
			return getattr(book,myKey).Date == myVal.Date
		if type(myVal) == str:
			return getattr(book,myKey).lower().strip() == myVal.lower().strip()
		else:
			return getattr(book,myKey) == myVal

	def isAnyOf(self,myString,myVals):
		if type(myString) == str:
			for word in myVals:
				if unicode(word.lower().strip()) == unicode(myString.lower().strip()): return True
			return False
		else:
			for v in myVals:
				if v == myString: return True
			return False

	def startsWith(self, myString, myVal):
		return myString.lower().startswith(myVal.lower().strip())

	def startsWithAnyOf(self, myString, myVals):
		myString = myString.strip()
		startsWith = False
		for word in myVals:
			if myString.lower().StartsWith(word.strip().lower()):
				startsWith = True
		return startsWith

	def containsAnyOf(self, myString, myVals):
		# example <<myString.containsAnyOf:val1,val2,val3>> 
		# or: <<The Adventures of Batman.ContainsAnyOf:Batman,Robin,Joker>>

		myString = myString.strip()

		for word in myVals:
			if word.lower().strip() in myString.lower(): return True
		return False

	def containsAllOf(self, myString, myVals):
		# example <<myString.containsAllOf:val1,val2,val3>> 
		# or: <<The Adventures of Batman.ContainsAllOf:Batman,Robin,Joker>>

		myString = myString.strip()
		
		for word in myVals:
			if not word.lower().strip() in myString.lower(): return False
		return True	
	
	def greater(self, myKey, myVal, book):
		if myKey in ['Number','AlternateNumber']:
			return self.toFloat(getattr(book,myKey)) > self.toFloat(myVal)
		elif type(myVal) == System.DateTime:
			return getattr(book,myKey).Date > myVal.Date
		elif type(myVal) == str:
			return getattr(book,myKey).lower() > myVal.lower()
		else:
			return getattr(book,myKey) > myVal

	def greaterEq(self, myKey, myVal, book):
		if myKey in ['Number','AlternateNumber']:
			return self.toFloat(getattr(book,myKey)) >= self.toFloat(myVal)
		elif type(myVal) == System.DateTime:
			return getattr(book,myKey).Date >= myVal.Date
		elif type(myVal) == str:
			return getattr(book,myKey).lower() >= myVal.lower()
		else:
			return getattr(book,myKey) >= myVal

	def less(self, myKey, myVal, book):
		if myKey in ['Number','AlternateNumber']:
			return self.toFloat(getattr(book,myKey)) < self.toFloat(myVal)
		elif type(myVal) == System.DateTime:
			return getattr(book,myKey).Date < myVal.Date
		elif type(myVal) == str:
			return getattr(book,myKey).lower() < myVal.lower()
		else:
			return getattr(book,myKey) < myVal

	def lessEq(self, myKey, myVal, book):
		if myKey in ['Number','AlternateNumber']:
			return self.toFloat(getattr(book,myKey)) <= self.toFloat(myVal)
		elif type(myVal) == System.DateTime:
			return getattr(book,myKey).Date <= myVal.Date
		elif type(myVal) == str:
			return getattr(book,myKey).lower() <= myVal.lower()
		else:
			return getattr(book,myKey) <= myVal

	def range(self, myKey, myVal, book):
		minVal = myVal[0]
		maxVal = myVal[1]
		fieldVal = getattr(book,myKey)
		if myKey in ['Number','AlternateNumber']:
			fieldVal = self.toFloat(fieldVal)
			if fieldVal == None: fieldVal = 0
			return fieldVal >= self.toFloat(minVal) and fieldVal <= self.toFloat(maxVal)
		elif type(myVal) == System.DateTime:
			return fieldVal.Date >= minVal.Date and fieldVal.Date <= maxVal.Date
		else:
			return fieldVal >= minVal and fieldVal <= maxVal

	def toFloat(self, myVal):
		# tries to convert a string myVal to float
		# returns None if not possible or string myVal is empty
	
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
			