'''
replaceData

plugin script for ComicRack to replace field content in the library
based on user-defined conditions
the rules are read from file replaceData.dat, located in the script directory

The CR Data Manager plugin is licensed under the Apache 2.0 software
license, available at: http://www.apache.org/licenses/LICENSE-2.0.html

v 0.1.15

by docdoom

images and icons used by permission of 600WPMPO and www.aha-soft.com

revision history

v 0.1.15
fixed - "do you want to see the log" dialogbox always appears behind the Comicrack Window
        (issue 34) (set ComicRack.Window  as parent window handle for all forms)
change - modular rewriting of forms
change - Contains compares now case insensitive
change - StartsWith compares now case insensitive
change - comparison for equality (==) is now case insensitive
change - comparison for less (<) is now case insensitive
change - comparison for lessEqual (<=) is now case insensitive
change - comparison for greater (>) is now case insensitive
change - comparison for greaterEq (>=) is now case insensitive
change - comparison for not equal (<>) is now case insensitive
fix - missing references to globalvars added
change - PageCount added to allowed keys
change - new modifier ContainsAnyOf (issue 28)
change - new modifier ContainsNot (may used as well as NotContains)
change - new modifier ContainsAllOf (issue 40)
change - if no value was modified by the DM, only "book xxx was touched" is written to logfile
change - new modifier NotContainsAnyOf
change - new modifier StartsWithAnyOf
change - new directive "#@ END_RULES"
change - new class "parser"
change - new class "ruleFile" (encapsulated reading and writing the DATFILE)
fix - exception when Null value was used in Range modifier
change - when error was raised by compiling code a MessageBox will show the error
...
r105
change - Configurator form re-written
change - basic Search functionality in Configurator
...
r106
change - first rudimentary GUI written (no functionality yet)
...
r109
change - ComicRack version check at start (min is 0.9.165)
change - basic GUI functionality
...
r111
change - new directive #@ GROUP
change - added combobox to find group header in textbox
change - textclips (like commentary line, group header etc. can be added via GUI)
change - rule editor position set to CenterParent
fixed - 'setvalue' was not recognized as a valid modifier
fixed - exception if file in rule editor is not the DatFile and combobox group selector is selected
...
r113
fixed - sometimes selected text in rule set is overwritten by inserted rule (GUI)
fixed - criterion or setvalue are not added to rule if already in there (GUI)
change - buttons for deleting content of textboxes for criteria and setvalue (GUI)
change - group names are checked if already used
fixed - Contains... methods in class parser rewritten (unexpected results when leading
        or trailing blanks where attached to values)
fixed - exception when a criterion with apostrophe or quotation mark was written to the log file
        (issue 36)
...
r114
change - save and close added to configurator menustrip
change - option to backup and restore the rule set (issue 30)
change - DMProc is no longer added to Tags but written as a custom value (issue 33)
..
r115
change - new allowed fields: alternateNumber and alternateCount (issue 44)
fixed - comboModifiers does not match comboCriteria and comboValues (issue 48)
change - option to select line by line number (issue 49)
...
r117
change - GUI: delete rule from rule set
change - GUI: re-engineer rule
change - menu strip upgraded
...
r121
change - new allowed fields: Title
fixed - unexpected behavior with book numbers like '5AU', 'Minus 1', '¼', fixed with
        function 'stringToFloat'
change - rule editor is now dropdown option in CR toolbar (form MainForm is obsolete)
change - range modifier is not selectable for string fields anymore in GUI
fixed - group header combo box was not updated when backup of rule set was loaded
...
r125
change - parser directive '#@ END_GROUP' added (issue 56)
change - new list ruleFile.pseudoNumericalKeys (Number, AlternateNumber)
change - new modifier Add for string type fields (non-multi value) (issue 32)
change - new modifier Replace for string type fields (non-multi value) (issue 32)
change - new modifier Remove for string type fields (non-multi value) (issue 32)
fixed - range modifiers for multivalue keys are now restricted to the elements of ruleFile.allowedKeyModifiersMulti (issue 55)
...
r128
change - new modifier NotStartsWith
change - new modifier NotStartsWithAnyOf
change - new value modifier RemoveLeading (leading and trailing blanks are respected) (issue 53)
fixed - StringReplace modifier does not ignore leading or trailing blanks anymore
change - added directives #@ AUTHOR, #@ NOTES, #@ END_NOTES (issue 59)
change - added all missing fields of type string, numeric, multi-value
change - when book was touched the process date is now written to CustomValue 'DataManager.processed'
         (this was it is only displayed when turned on with ShowCustomScriptValues = true in ComicRack.ini) 
...
r129
fixed - comparer >= etc. did not work as expected with numerical values
fixed - progressbar was hidden behind CR window when clicked (removed MainWindow handle, issue 52)
...
r133
change - allowed vals and modifiers are read from dataman.ini


>> revision history for older releases is at http://code.google.com/p/cr-replace-data/wiki/RevisionLog

ideas:
todo: modifier Before
todo: modifier After
todo: use In as modifier in keys
     e.g. <<Number.In:1,3,8>>
todo: add RegExp as modifier
todo: simulation instead of actual replacing of data
------------------------------------------------------
'''

import clr
import sys
import re
import System
import System.Text
from System import String
from System.IO import File,  Directory, Path, FileInfo, FileStream
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *


# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

DEBUG__ = False

import globalvars
import utils
#from utils import parser
#from utils import comparer
#from utils import nullToZero
from utils import *
#from mainform import mainForm
from displayResultsForm import displayResultsForm
from aboutForm import aboutForm
from progressForm import progressForm
from configuratorForm import configuratorForm
from utils import ruleFile

from time import localtime, strftime

sys.path.append(globalvars.FOLDER)

def debug (s):
	if DEBUG__ == True:
		print str(s)
	return

def writeVersion():
	myIni = utils.iniFile()
	myIni.write('Version','0.1.15 r133')
	
def writeCode(s, level, linebreak):
	''' 
	writes code to dataMan.tmp
	parameters: 
	s - string to write (str)
	level - indentation level (int)
	linebreak - add linebreak? (bool)
	'''
	s = str(s)
	prefix = '\t' * level
	s = prefix + s
	if linebreak == True: s += '\n'
	try:
		File.AppendAllText(globalvars.TMPFILE, s)
		
	except Exception, err:
		print "Error in function writeCode: ", str(err)

#def parsedCode():
#	try:
#		return File.ReadAllText(globalvars.TMPFILE)
#	except Exception, err:
#		print "Error in function parsedCode: ", str(err)


		
def parseString(s):
	# todo: this belongs in class ruleFile
	
	# read a line from replaceData.dat and generate python code from it
	
	myCrit = ''				# this will later contain the left part of the rule
	myNewVal = ''			# this will later contain the new value (right part of rule)
	myModifier = ''			# the modifier (like Contains, Range, Calc etc.)

	rules = utils.ruleFile()
	allowedKeys = rules.allowedKeys
	allowedVals = rules.allowedVals
	numericalKeys = rules.numericalKeys
	pseudoNumericalKeys = rules.pseudoNumericalKeys
	multiValueKeys = rules.multiValueKeys
	
	myParser = utils.parser()
	myParser.validate(s)
	if myParser.err:
		File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (%s)\nline: %s)" % (myParser.error, s))
		return 0
	
	a = s.split("=>")

	# some preparation for the criteria part:
	a[0] = String.Trim(a[0])
	#if apostrophes were already escaped by '\' remove the escaping \:
	a[0] = a[0].replace(r"\'", r"'")
	a[0] = a[0].replace(r'\"', r'"')
	# now escape all apostrophes with '\'
	a[0] = a[0].replace('\'', '\\\'')		# apostrophes
	a[0] = a[0].replace('\"', '\\\"')		# quotation marks
	
	# split the string and retrieve the criteria (left part) and newValues (right part) 
	# store those in lists
	try:		
		criteria = a[0].split(">>")			
		newValues = a[1].split(">>")
	except Exception, err:
		print str(err)
	
	# iterate through each of the criteria
	for c in criteria:
		#i = len(c)
		if len(c) > 0:
			c = String.Trim(String.replace(c,"<<",""))
			myKey = ''  # only to reference it
			if String.find(c,':') > 0:
				tmp = c.split(":",1)
				tmp2 = tmp[0].split(".",1)
				myKey = tmp2[0]
				try:
					myModifier = tmp2[1]
				except Exception, err:
					myModifier = ""
			else:
				File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0

			if c <> "" and not (myKey in allowedKeys) and not myKey.startswith('CustomValue'):
				File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			myOperator = "=="
			# handling if modifier is appended to field
			# like Volume.Range:1961, 1963
			try:
				if myModifier <> "":
					if str.lower(myModifier) == "range":
						myOperator = "in range"
					elif str.lower(myModifier) == 'is':
						myOperator = '=='
					elif str.lower(myModifier) == "not":
						myOperator = "<>"
					elif str.lower(myModifier) == "contains":
						myOperator = ""
					elif str.lower(myModifier) == "greater":
						myOperator = ">"
					elif str.lower(myModifier) == "greatereq":
						myOperator = ">="
					elif str.lower(myModifier) == "less":
						myOperator = "<"
					elif str.lower(myModifier) == "lesseq":
						myOperator = "<="
					elif str.lower(myModifier) == "startswith":
						myOperator = ""
					elif str.lower(myModifier) == 'notstartswith':
						myOperator = ''
					elif str.lower(myModifier) == 'startswithanyof':
						myOperator = ''
					elif str.lower(myModifier) == 'notstartswithanyof':
						myOperator = ''
					elif str.lower(myModifier) == "containsanyof":
						myOperator = ""
					elif str.lower(myModifier) == "notcontainsanyof":
						myOperator = ""
					elif str.lower(myModifier) == "containsnot" or str.lower(myModifier) == "notcontains":
						myModifier = "ContainsNot"
					elif str.lower(myModifier) == "containsallof":
						myOperator = ""
					else:
						File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid modifier %s)\nline: %s)" % (myModifier, s))
						return 0
											
			except Exception, err:
				MessageBox.Show("error at parseString: %s" % str(err))
				return

			myVal = tmp[1]

			if myOperator == "in range":		# must only be used with numerical keys
				
				tmp = myVal.split(",")
				val1 = int(nullToZero(stringToFloat(tmp[0])))
				val2 = int(nullToZero(stringToFloat(tmp[1])))
				myVal = "%d, %d" % (val1, val2 + 1)
				if myKey in numericalKeys or myKey in pseudoNumericalKeys:	# ('Number','AlternateNumber'):
					myCrit = myCrit + ("int(stringToFloat(nullToZero(book.%s))) %s (%s) and " % (myKey, myOperator, myVal))
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "Range modifier cannot be used in %s field" % (myKey))
					return 0
			# ---------------------------------------------------------------------------
			# now begins the interesting part for fields Number/Autonumber which is stored as 
			# a string but should be treated like a numerical value
			elif myOperator in ('==', '>', '>=', '<', '<=') and myKey in pseudoNumericalKeys:	# (myKey == 'Number' or myKey == 'AlternateNumber'):
				if str.Trim(myVal) == '':
					# fix issue 31
					myCrit = myCrit + ('str(book.%s) %s \'\' and ' % (myKey, myOperator))
				else:
					# if the current value of book.Number is Null it has to be converted to
					# 0 before it can be converted to float
					if myOperator == '==':
						# if operator is == then we need an exact compare
						myVal = str(nullToZero(myVal))
						myCrit += 'nullToZero(book.%s) %s \'%s\' and ' % (myKey, myOperator, myVal)
					else:
						# if operator is <, > and so forth we have to simulate those
						# values as numeric, so we use stringToFloat
						myVal = nullToZero(stringToFloat(myVal))
						myCrit = myCrit + ('nullToZero(stringToFloat(book.%s)) %s %s and ' % (myKey, myOperator, myVal))
					pass
			# end of extra handling of Number field
			# ----------------------------------------------------------------------------
			elif str.lower(myModifier) == "contains" and myKey not in numericalKeys:
				myCrit = myCrit + 'comp.contains(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			
			elif str.lower(myModifier) == "containsanyof": # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsAnyOf modifier cannot be used in %s field" % (myKey))
					return 0
			elif str.lower(myModifier) == "notcontainsanyof":
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.notContainsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "NotContainsAnyOf modifier cannot be used in %s field" % (myKey))
					return 0
				
			elif str.lower(myModifier) == "containsallof": # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsAllOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsAllOf modifier cannot be used in %s field" % (myKey))
					return 0

			elif str.lower(myModifier) == "containsnot":
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsNot(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsNot modifier cannot be used in %s field" % (myKey))
					return 0
			elif myModifier.lower() == "notstartswith" and myKey not in numericalKeys:
				myCrit = myCrit + ("comp.startsWith(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) == False and " % (myKey,myVal))
			elif myModifier.lower() == "startswith" and myKey not in numericalKeys:
				myCrit = myCrit + ("comp.startsWith(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,myVal))
				#myCrit = myCrit + ("book.%s.startswith(\"%s\") and " % (myKey,myVal))
			elif str.lower(myModifier) == "startswithanyof" or myModifier.lower() == 'notstartswithanyof' : # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					if myModifier.lower() == 'startswithanyof':
						myCrit = myCrit + 'comp.startsWithAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
					else:
						myCrit = myCrit + 'comp.startsWithAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == False and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "StartsWithAnyOf and NotStartsWithAnyOf modifiers cannot be used in %s field" % (myKey))
					return 0
			elif myOperator == '==' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.equals(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,myVal)
			elif myOperator == '<' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.less(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.lessEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greater(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greaterEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<>' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.notEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			else:
				# numerical values in CR are -1 if Null
				if myKey in numericalKeys and str.Trim(myVal) == '':
					myVal = -1
				if myKey in numericalKeys:
					myCrit = myCrit + ("book.%s %s %s and " % (myKey, myOperator, myVal))
				
			
	myCrit = "if " + String.rstrip(myCrit, " and") + ":"
	writeCode(myCrit,1,True)

	writeCode("f.write(book.Series.encode('utf-8') + ' v' + str(book.Volume) + ' #' + book.Number.encode('utf-8') + ' was touched \\t(%s)\\n')" % a[0], 2, True)
	
	# iterate through each of the newValues
	for n in [n for n in newValues if n.strip() <> '']:
		if len(n) > 0:
			n = n.replace('<<','').lstrip()
			str.lower(n).replace('.setvalue','')		# SetValue is default
			if String.find(n,':') > 0:
				# get key part (substring before ':')
				tmp = n.split(":",1)
				myKey = tmp[0]
				myModifier = ''
				if String.find(myKey,'.') > 0:
					tmp3 = myKey.split('.')
					myKey = tmp3[0]
					myModifier = tmp3[1]
			else:
				File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (missing \':\' after \'%s\')\nline: %s)" % (myKey, s))			
				return 0
			if not (myKey in allowedVals):
				File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			# to do: handling if function is appended to field
				
			myVal = tmp[1]
			writeCode("myOldVal = str(book.%s)" % myKey, 2, True)

			if str.lower(myModifier) == 'setvalue':
				myModifier = ''
				
			if myModifier <> "":
				if str.lower(myModifier) == "calc":
					if myKey not in numericalKeys and myKey not in pseudoNumericalKeys:	# <> 'Number':
						myVal = String.replace(myVal,'{','str(book.')
					else:
						myVal = String.replace(myVal,'{','int(book.')
					myVal = String.replace(myVal,'}',')')
					if myKey in pseudoNumericalKeys:	# == 'Number':
						writeCode("book.%s = str(%s)" % (myKey, myVal), 2, True)
					else:
						writeCode("book.%s = %s" % (myKey, myVal), 2, True)
				if str.lower(myModifier) == "add":
					if myKey in numericalKeys + pseudoNumericalKeys:	# == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Add modifier cannot be used in %s field" % (myKey))
						return 0
					if myKey in multiValueKeys:
						if len(String.Trim(myVal)) == 0:
							File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
							File.AppendAllText(globalvars.ERRFILE, "Add modifier needs 1 argument")
							return 0
						else:
							writeCode('book.%s = multiValueAdd(book.%s,"%s")' % (myKey, myKey, myVal), 2, True)
					else: 				# myKey in allowedKeys
						writeCode('book.%s = stringAdd(book.%s,"%s")' %  (myKey, myKey, myVal), 2, True)
				if str.lower(myModifier) == "replace":
					tmpVal = myVal.split(',')
					if len(tmpVal) <= 1:
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Replace modifier needs 2 arguments")
						return 0
					if myKey in numericalKeys + pseudoNumericalKeys:	# == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Replace modifier cannot be used in %s field" % (myKey))
						return 0
					elif myKey in multiValueKeys:
						writeCode ('book.%s = multiValueReplace(book.%s,"%s","%s")' % (myKey, myKey, tmpVal[0], tmpVal[1]), 2, True)
					else:
						writeCode('book.%s = stringReplace(book.%s,"%s","%s")' % (myKey, myKey, tmpVal[0], tmpVal[1]), 2, True)
							
				if str.lower(myModifier) == "remove":
					if len(String.Trim(myVal)) == 0:
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Remove modifier needs 1 argument")
						return 0
					if myKey in numericalKeys or myKey in pseudoNumericalKeys:	# == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Remove modifier cannot be used in %s field" % (myKey))
						return 0
					if myKey in multiValueKeys:
						writeCode('book.%s = multiValueRemove(book.%s,"%s\")' % (myKey, myKey, myVal), 2, True)
					else:
						writeCode('book.%s = stringRemove(book.%s,"%s\")' % (myKey, myKey, myVal), 2, True)
				if myModifier.lower() == 'removeleading':
					if len(String.Trim(myVal)) == 0:
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "RemoveLeading modifier needs 1 argument")
						return 0
					if myKey in numericalKeys or myKey in (pseudoNumericalKeys + multiValueKeys):	# == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Remove modifier cannot be used in %s field" % (myKey))
						return 0
					writeCode('book.%s = stringRemoveLeading(book.%s,"%s\")' % (myKey, myKey, myVal), 2, True)

			else:

				if myKey in numericalKeys:
					if len(myVal) == 0:
						writeCode("book.%s = \'\'\n" % (myKey), 2, True)
					else:
						writeCode("book.%s = %s\n" % (myKey, myVal), 2, True)
				else:
					writeCode("book.%s = \"%s\"" % (myKey, myVal), 2, True)
				myNewVal = myNewVal + ("\t\tbook.%s = \"%s\"" % (myKey, myVal)) 

			writeCode("myNewVal = str(book.%s)" % myKey, 2, True)
			writeCode("if myNewVal <> myOldVal:", 2, True)	
			writeCode("f.write('\\tbook.%s - old value: ' + myOldVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode("f.write('\\tbook.%s - new value: ' + myNewVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode("book.SetCustomValue(\'DataManager.processed\',strftime(\'%Y-%m-%d\', localtime()))", 3, True)
			
			writeCode("else:", 2, True)
			writeCode("pass",3,True)
			# writeCode("f.write('\\t%s - old value was same as new value\\n')" % (myKey), 3, True)
	return -1
	

def dmConfig():
	
	FOLDER = FileInfo(__file__).DirectoryName + "\\"
	
	theDLL = Path.Combine(FOLDER, 'crdmcgui.dll')
	
#	clr.AddReferenceToFileAndPath(theDLL)
	clr.AddReference('crdmcgui-fm3ce.dll')
#	from crdmcgui import gui	

#	clr.AddReference('crdmcgui.dll')
#
	from crdmcgui import *
	
	dmGUI = gui(globalvars.DATFILE)
	dmGUI.ShowDialog(ComicRack.MainWindow)

	return

	# old version:
	form = configuratorForm()
	form.setFile(globalvars.DATFILE)
	form.Text = 'Data Manager Configurator %s' % globalvars.VERSION
	form.ShowDialog(ComicRack.MainWindow)
	form.Dispose()

def crVersion():
	minVersion = '0.9.164'		# we need CR 0.9.164 minimum (for custom values)
	vMin = 0 + 9000 + 164
	myVersion = ComicRack.App.ProductVersion	# get the installed CR version number
	v = myVersion.split('.')
	vMyVersion = (int(v[0]) * 1000000) + (int(v[1]) * 1000) + int(v[2])
	if vMyVersion < vMin:		# if actual version is lower than minimum version: return False
		MessageBox.Show(
		'You have only CR version %s installed.\nPlease install at least version %s of ComicRack first!' % (myVersion,minVersion),
		'Data Manger for ComicRack %s' % globalvars.VERSION)
		return False
	return True

def addALotOfBooks():
	i = 1001
	while True:
		theBook = ComicRack.App.AddNewBook(False)
		theBook.Series = 'Automatic Series'
		theBook.Number = str(i)
		if i == 5000:
			break
		i += 1
	return

# ============================================================================      
# hook to run the configScript
#@Name	 Data Manager configuration
#@Key    data-manager
#@Hook   ConfigScript
# ============================================================================      
def dataManagerConfig():
	dmConfig()


# ============================================================================ 
# hook to run the main dataManager loop
#@Name	Data Manager
#@Image dataMan16.png
#@Key	data-manager
#@Hook	Books
# ============================================================================     

def replaceData(books):


	#for book in [book for book in books if book.GetCustomValue('my_Val') <> None]: # works
	#for book in [book for book in books if book.GetCustomValue('my_Val') < '2']: # works strange if used with pseudo numbers
	# sample how to retrieve the custom values for a book:
	#	for book in books:
	#		myObj = book.GetCustomValues()
	#		for o in myObj:
	#			print o.Key
	#			print o.Value
	#	return ''

	ERROR_LEVEL = 0

	if not crVersion():
		return
	
	try:
		File.Delete(globalvars.TMPFILE)
		File.Delete(globalvars.ERRFILE)
	except Exception, err:
		pass
	
	# check if configuration exists
	if not File.Exists(globalvars.DATFILE):
		MessageBox.Show('Please use the Data Manager Configurator first!','Data Manager %s' % globalvars.VERSION)
		return

	# check if configuration has been saved once
	if not File.Exists(globalvars.CHKFILE):
		MessageBox.Show('Please save your configuration first!','Data Manager %s' % globalvars.VERSION)
		return

	writeCode('try:', 0, True)
	
	progBar = progressForm()
	progBar.Show()
#	progBar.ShowDialog(ComicRack.MainWindow)
	
	writeCode('import System',1,True)
	writeCode('from System.Windows.Forms import MessageBox',1,True)
	writeCode('from time import localtime, strftime',1,True)
	writeCode('from globalvars import *',1,True)
	writeCode('from utils import *',1,True)
	writeCode('comp = comparer()',1,True)
	
	try:
		s = File.ReadAllLines(globalvars.DATFILE)
		i = 0
		s = [line for line in s if str.Trim(line) <> '']
		for line in s:
			i += 1

			if not line.StartsWith('#'):	# don't run this on commentary lines
											# todo: handle parser directives starting with #@

				if not parseString(line):	# syntax error found, break parsing the rule set
					error_message = File.ReadAllText(globalvars.ERRFILE)
					MessageBox.Show("Error in line %d!\n%s" % (i, str(error_message)),"CR Data Manager %s - Parse error" % globalvars.VERSION)
					ERROR_LEVEL = 1
					break
			if line.startswith('#@ END_RULES'):
				break
			
	except Exception, err:
		MessageBox.Show('Something bad happened during code generation:\n%s' % str(err),'Data Manager for ComicRack %' % globalvars.VERSION)
		progBar.Dispose()

	writeCode('except Exception,err:', 0, True)
	writeCode('MessageBox.Show (\"Error in code generation: %s\" % str(err))', 1, True)
	
	if ERROR_LEVEL == 0:
		theCode = File.ReadAllText(globalvars.TMPFILE)
		debug("code generated by CR Data Manager: \n%s" % theCode)
			
#		progBar = progressForm()
#		progBar.ShowDialog()
		progBar.setMax(books.Length)
		touched = 0
		f=open(globalvars.LOGFILE, "w")	# open logfile
		for book in books:
			touched += 1
			progBar.setValue(touched)
			try:
				exec (theCode)
				
			except Exception, err:
				MessageBox.Show('Error while executing the rules. \n%s\nPlease check your rules.' % str(err), 'Data Manager - Version %s' % globalvars.VERSION)
				ERROR_LEVEL = 1
		
		f.close()				# close logfile

		progBar.Dispose()
		
		if ERROR_LEVEL == 0:
			msg = "Finished. I've inspected %d books.\nDo you want to take look at the log file?" % (touched)
	
			form = displayResultsForm()
			form.configure(msg)
			form.ShowDialog(ComicRack.MainWindow)
			form.Dispose()

			if form.DialogResult == DialogResult.Yes:
	
				form = configuratorForm()
				form.setFile(globalvars.LOGFILE)
				form.Text = 'Data Manager Logfile %s' % globalvars.VERSION
				form.ShowDialog(ComicRack.MainWindow)
				form.Dispose()

	try:
		#File.Delete(TMPFILE)
		File.Delete(globalvars.ERRFILE)
	except Exception, err:
		pass
	

# todo: move stringToFloat to utils.py
def stringToFloat(myVal):
	# tries to convert a string myVal to float
	# returns None if not possible or string myVal is empty

	try:
		return float(myVal)
	except Exception, err:
		pass

	s = ''
	s = str(myVal).lower().strip()
	
	if s == '': return None

	s = s.replace(chr(188),'.25')
	s = s.replace(chr(189),'.5')
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

		