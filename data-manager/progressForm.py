import System.Drawing
import System.Windows.Forms
import System.Threading
from System.IO import File

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
from globalvars import *

import dmutils
from dmutils import *


dmString = dmString()
userIni = iniFile(globalvars.USERINI)
userIni.write('LastScanErrors',0)
stop_the_Worker = False
ERRCOUNT = 0

theLog = ""

# initialize this with
# 1.) for the run over the books:
# theForm = progressForm(PROCESS_BOOKS, books)
# 2.) for parsing the code:
# theForm = progressForm(PROCESS_CODE)


class progressForm(Form):
	def __init__(self, theProcess = 0, books = None):
		self.InitializeComponent()
		#self.progValue = 0
		#self.labelText = theText
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.Text = 'Data Manager for ComicRack %s' % globalvars.VERSION
		self.theProcess = theProcess
		#self.theCode = theCode
		self.theBooks = books
		self.errorLevel = 0
		self.cancelledByUser = False
		self.stepsPerformed = 0
		self.maxVal = 0
		userIni = iniFile(globalvars.USERINI)
		self.dateTimeFormat = userIni.read('DateTimeFormat')	
		globals()['stop_the_Worker'] = False
	
	def InitializeComponent(self):
		self._progressBar = System.Windows.Forms.ProgressBar()
		self._label1 = System.Windows.Forms.Label()
		self._backgroundWorker1 = System.ComponentModel.BackgroundWorker()
		self._buttonCancel = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# progressBar
		# 
		self._progressBar.Location = System.Drawing.Point(12, 39)
		self._progressBar.Name = "progressBar"
		self._progressBar.Size = System.Drawing.Size(413, 23)
		self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._progressBar.TabIndex = 0
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.BackColor = System.Drawing.SystemColors.Control
		self._label1.Location = System.Drawing.Point(13, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(22, 13)
		self._label1.TabIndex = 1
		self._label1.Text = "xxx"
		# 
		# backgroundWorker1
		# 
		self._backgroundWorker1.WorkerReportsProgress = True
		self._backgroundWorker1.WorkerSupportsCancellation = True
		self._backgroundWorker1.DoWork += self.BackgroundWorker1DoWork
		self._backgroundWorker1.ProgressChanged += self.BackgroundWorker1ProgressChanged
		self._backgroundWorker1.RunWorkerCompleted += self.BackgroundWorker1RunWorkerCompleted
		#self._backgroundWorker1.CancellationPending += self.BackgroundWorker1Cancellation
		# 
		# buttonCancel
		# 
		self._buttonCancel.Location = System.Drawing.Point(185, 71)
		self._buttonCancel.Name = "buttonCancel"
		self._buttonCancel.Size = System.Drawing.Size(75, 23)
		self._buttonCancel.TabIndex = 2
		self._buttonCancel.Text = "Cancel"
		self._buttonCancel.UseVisualStyleBackColor = True
		self._buttonCancel.Click += self.ButtonCancelClick
		# 
		# progressForm
		# 
		self.ClientSize = System.Drawing.Size(436, 106)
		self.Controls.Add(self._buttonCancel)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._progressBar)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "progressForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "progressForm"
		self.FormClosing += self.ProgressFormFormClosing
		self.FormClosed += self.ProgressFormFormClosed
		self.Load += self.ProgressFormLoad
		self.Shown += self.ProgressFormShown
		self.ResumeLayout(False)
		self.PerformLayout()


	def ProgressFormLoad(self, sender, e):
		pass
	




	def BackgroundWorker1DoWork(self, sender, e):

		if self.theProcess == 0:		# just for testing
			i = 0
			while i <= 100:
				i += 1
				# Report progress to 'UI' thread
				self._backgroundWorker1.ReportProgress(i)
				# Simulate long task
				System.Threading.Thread.Sleep(100)
			return

		# ------------------------------------------------------
		# parse the code line by line:
		# ------------------------------------------------------
		
		if self.theProcess == globalvars.PROCESS_CODE:

			globalvars.THECODE = []
			userIni = iniFile(globalvars.USERINI)
			userIni.write('LastScanErrors',0)
			writeCode('try:', 0, True)	
			writeCode('import System',1,True)
			writeCode('from System.Windows.Forms import MessageBox',1,True)
			writeCode('from time import localtime, strftime',1,True)
			writeCode('from globalvars import *',1,True)
			writeCode('from dmutils import *',1,True)
			writeCode('userIni = iniFile(globalvars.USERINI)',1,True)
			writeCode('comp = comparer()',1,True)
			writeCode('dmString = dmString()',1,True)
			writeCode('multiValue = multiValue()',1,True)
			writeCode('dmDateTime = dmDateTime()',1,True)
			writeCode('dmNumeric = dmNumeric()',1,True)
			writeCode('dmYesNo = dmYesNo()',1,True)
			writeCode('dmMangaYesNo = dmMangaYesNo()',1,True)
			writeCode('breakAfterFirstError = userIni.read("BreakAfterFirstError")',1,True)
			writeCode('ERRCOUNT = 0',1,True)
			writeCode('def writeError(f,error, action):',1,True)
			writeCode	("myLog = ('\\t*************************************************\\n')",2,True)
			writeCode	("myLog += ('\\tan error happened here! Please check your actions\\n')",2,True)
			writeCode	("myLog += ('\\taction: %s\\n' % action)",2,True)
			writeCode	("myLog += ('\\terror : %s\\n' % str(error))",2,True)
			writeCode	("myLog += ('\\t*************************************************\\n')",2,True)
			writeCode	("return myLog",2,True)
			
			s = File.ReadAllLines(globalvars.DATFILE)
			self.maxVal = len(s)
			self._progressBar.Maximum = self.maxVal
			self._progressBar.Step = 1
#			i = 0
			for line in s:
				if not self._backgroundWorker1.CancellationPending: 
					self.stepsPerformed += 1
					# note that ReportProgress needs an argument!
					self._backgroundWorker1.ReportProgress(self.stepsPerformed / self.maxVal * 100)
	
					try:
						if not line.StartsWith('#') and not line.strip() == '':	# don't run this on commentary lines
																				# todo: handle parser directives starting with #@
	
							if not parseString(line):	# syntax error found, break parsing the rule set
								error_message = unicode(File.ReadAllText(globalvars.ERRFILE))
								MessageBox.Show("Error in line %d!\n%s" % (self.stepsPerformed, error_message),"CR Data Manager %s - Parse error" % globalvars.VERSION)
								self.errorLevel = 1
								break
						if line.startswith('#@ END_RULES'):
							break
					except Exception, err:
						pass
				else:
					self.cancelledByUser = True
					return
				
			#progBar.Dispose()

			writeCode('except Exception,err:', 0, True)
			writeCode('MessageBox.Show (\"Error in code generation: %s\" % str(err))', 1, True)

			#writeCode('global theLog',0,True)

			self.Close()
				

		# ------------------------------------------------------
		# run the parsed code over the books:
		# ------------------------------------------------------
		userIni = iniFile(globalvars.USERINI)
		dtStarted = System.DateTime.Now

		if self.theProcess == globalvars.PROCESS_BOOKS:
			self.maxVal = self.theBooks.Length
			self._progressBar.Maximum = self.maxVal
			self._progressBar.Step = 1
			f=open(globalvars.LOGFILE, "w")	# open logfile

			for book in self.theBooks:
				if not self._backgroundWorker1.CancellationPending: 
					self.stepsPerformed += 1
					self._backgroundWorker1.ReportProgress(self.stepsPerformed / self.maxVal * 100)
					try:
						myCode = ''
						for line in globalvars.THECODE:
							if line.strip() <> '':
								myCode += line
						# print the generated code once to the debug window:
						if self.stepsPerformed == 1: print myCode
						exec(myCode)


						
					except Exception, err:
						print str(Exception.args)
						MessageBox.Show('An unhandled error occurred while executing the rules. \n%s\nPlease check your rules.' % str(err), 'Data Manager - Version %s' % globalvars.VERSION)
						self.errorLevel = 1
						break
					
				else:
					theLog += ('\n\nExcecution cancelled by user.')
					self.cancelledByUser = True
					break
				
			#f.close()				# close logfile

			dtEnded = System.DateTime.Now
			dtDuration = dtEnded - dtStarted
			userIni.write('ParserStarted',str(dtStarted))
			userIni.write('ParserEnded',str(dtEnded))
			userIni.write('ParserDuration',str(dtDuration))

			if userIni.read('LastScanErrors') <> '0':
				MessageBox.Show('There were errors in your rules. You really should check the logfile!')

			#MessageBox.Show(theLog)
			f.write(theLog)
			f.close()
		return
			

	def BackgroundWorker1ProgressChanged(self, sender, e):
		# progressBar.Value = xxx  did not update the progressBar properly
		# so we use PerformStep()
		self._progressBar.PerformStep()
		if self.theProcess == globalvars.PROCESS_BOOKS:
			self._label1.Text = 'Data Manager worked on %d books' % self.stepsPerformed
		elif self.theProcess == globalvars.PROCESS_CODE:
			self._label1.Text = 'Data Manager parsed %d rules' % self.stepsPerformed
		return

	def BackgroundWorker1RunWorkerCompleted(self, sender, e):
		self.Close()
		pass

	def ProgressFormShown(self, sender, e):
		self._backgroundWorker1.RunWorkerAsync()
		
	def ButtonCancelClick(self, sender, e):
		self._backgroundWorker1.CancelAsync()
		pass
	
	def ProgressFormFormClosed(self, sender, e):
		self._backgroundWorker1.CancelAsync()

		
	def ProgressFormFormClosing(self, sender, e):
		self._backgroundWorker1.CancelAsync()

	def BackgroundWorker1Cancellation(self, sender, e):
		globals()['stop_the_Worker'] = True


def parseString(s):
	# todo: this belongs in class ruleFile
	
	# read a line from replaceData.dat and generate python code from it
	
	myCrit = ''				# this will later contain the left part of the rule
	myNewVal = ''			# this will later contain the new value (right part of rule)
	myModifier = ''			# the modifier (like Contains, Range, Calc etc.)


	rules = dmutils.ruleFile()
	allowedKeys = rules.allowedKeys
	allowedVals = rules.allowedVals
	numericalKeys = rules.numericalKeys
	dateTimeKeys = rules.dateTimeKeys
	pseudoNumericalKeys = rules.pseudoNumericalKeys
	multiValueKeys = rules.multiValueKeys
	yesNoKeys = rules.yesNoKeys
	mangaYesNoKeys = rules.mangaYesNoKeys
	
	dmString = dmutils.dmString()

	myParser = dmutils.parser()
	myParser.validate(s)
	if myParser.err:
		File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (%s)\nline: %s)" % (myParser.error, s))
		return 0
	
	a = s.split("=>")

	# this will be used later when an error is written to the logfile:
	theActionString = a[1]
	theActionString = theActionString.replace('\'','`')
	theActionString = theActionString.replace('\\','\\\\')

	writeCode('theActionString = \"%s\"' % theActionString, 1, True)

	# todo: checked up here
	
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

	# todo: checked up here
	
	# ----------------------------------------------------------------
	# iterate through each of the criteria
	# ----------------------------------------------------------------

	for c in criteria:
		#i = len(c)
		myCustomField = dmutils.customFields()
		if len(c) > 0:
			c = String.Trim(String.replace(c,"<<",""))
			myKey = ''  # only to reference it
			
			if c.lower().startswith('custom'):
				try:
					myCustomField.parseRule(c)
					myKey = myCustomField.theKey
					myModifier = myCustomField.theModifier
					myVal = myCustomField.theVal
				except Exception, err:
					print str(err)
			elif String.find(c,':') > 0:
				tmp = c.split(":",1)			# split key+modifier and value part
				tmp2 = tmp[0].split(".",1)		# split key and modifier
				myKey = tmp2[0]					# this is the key
				myVal = tmp[1]					# this is the value
				
				try:
					myModifier = tmp2[1]
				except Exception, err:
					myModifier = ""


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
					elif str.lower(myModifier) == 'isanyof':
						myOperator = ''
					elif str.lower(myModifier) == 'notisanyof':
						myOperator = ''
					else:
						File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid modifier %s)\nline: %s)" % (myModifier, s))
						return 0
											
			except Exception, err:
				MessageBox.Show("error at parseString: %s" % str(err))
				return


			# --------------------------------------------------
			# special handling for custom fields
			# --------------------------------------------------
			
			if myKey.lower().startswith('custom'):
				myKeyName = myCustomField.customFieldName(myKey)
				if myVal.strip() == '': 
					myCrit += 'book.GetCustomValue(\'%s\') %s None' % (myKeyName,myOperator)
				else:
					myCrit += 'str(book.GetCustomValue(\'%s\')).lower() %s \'%s\'.lower()' % (myKeyName,myOperator,myVal)
			elif myOperator == "in range":		# must only be used with numerical keys
				
				tmp = myVal.split(",")
		
				if myKey in numericalKeys or myKey in pseudoNumericalKeys:
					val1 = float((nullToZero(dmString.toFloat(tmp[0]))))
					val2 = float(nullToZero(dmString.toFloat(tmp[1])))
				elif myKey in dateTimeKeys:
					val1 = tmp[0]
					val2 = tmp[1] + ' 23:59:59'

				if myKey in numericalKeys or myKey in pseudoNumericalKeys:	# ('Number','AlternateNumber'):
					myVal = "%d, %d" % (val1, val2 + 1)
					myCrit = myCrit + ("int(dmString.toFloat(nullToZero(book.%s))) %s (%s) and " % (myKey, myOperator, myVal))
				elif myKey in dateTimeKeys:
					myCrit += 'book.%s >= System.DateTime.Parse(\'%s\') and book.%s <= System.DateTime.Parse(\'%s\') and ' % (myKey,val1,myKey,val2)

			# ---------------------------------------------------------------------------
			# now begins the interesting part for fields Number/Autonumber which is stored as 
			# a string but should be treated like a numerical value
			elif myOperator in ('==', '>', '>=', '<', '<=') and myKey in pseudoNumericalKeys:	# (myKey == 'Number' or myKey == 'AlternateNumber'):
				
				# todo: checked up here

				
				if str.Trim(myVal) == '':
					# fix issue 31
					# myCrit = myCrit + ('str(book.%s) %s \'\' and ' % (myKey, myOperator))
					# try this instead
					myCrit = myCrit + ('book.%s %s \'\' and ' % (myKey, myOperator))
				else:
					# if the current value of book.Number is Null it has to be converted to
					# 0 before it can be converted to float
					if myOperator == '==':
						# if operator is == then we need an exact compare
						myVal = nullToZero(myVal)
						# myVal = str(myVal)    # this would raise Exception if myVal = ininite symbol
						
						myCrit += 'nullToZero(book.%s) %s \'%s\' and ' % (myKey, myOperator, myVal)

					else:
						# if operator is <, > and so forth we have to simulate those
						# values as numeric, so we use stringToFloat


# range uses this:
						myVal = dmString.toFloat(nullToZero(myVal))
						myCrit += ("dmString.toFloat(nullToZero(book.%s)) %s (%s) and " % (myKey, myOperator, myVal))

# this gave false result (issue 71):
#						myVal = nullToZero(stringToFloat(myVal))		
#						myCrit = myCrit + ('nullToZero(stringToFloat(book.%s)) %s %s and ' % (myKey, myOperator, myVal))
					pass
			# end of extra handling of Number field
			# ----------------------------------------------------------------------------
			elif str.lower(myModifier) == "contains" and myKey not in numericalKeys:
				myCrit = myCrit + 'comp.contains(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			
			elif str.lower(myModifier) == "containsanyof": # and myKey not in numericalKeys:
				myCrit = myCrit + 'comp.containsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			elif str.lower(myModifier) == "notcontainsanyof":
				myCrit = myCrit + 'comp.notContainsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			elif str.lower(myModifier) == "containsallof": # and myKey not in numericalKeys:
				myCrit = myCrit + 'comp.containsAllOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			elif str.lower(myModifier) == "containsnot":
				myCrit = myCrit + 'comp.containsNot(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
			elif myModifier.lower() in ('isanyof','notisanyof'):
				if myModifier.lower() == 'isanyof':
					myCrit = myCrit + ('comp.isAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal))
				else:
					myCrit = myCrit + ('comp.isAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == False and ' % (myKey, myVal))
			elif myModifier.lower() == "notstartswith" and myKey not in numericalKeys:
				myCrit = myCrit + ("comp.startsWith(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) == False and " % (myKey,myVal))
			elif myModifier.lower() == "startswith" and myKey not in numericalKeys:
				myCrit = myCrit + ("comp.startsWith(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,myVal))
			elif str.lower(myModifier) == "startswithanyof" or myModifier.lower() == 'notstartswithanyof' : # and myKey not in numericalKeys:
				if myModifier.lower() == 'startswithanyof':
					myCrit = myCrit + 'comp.startsWithAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					myCrit = myCrit + 'comp.startsWithAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == False and ' % (myKey, myVal)
			elif myKey in dateTimeKeys:
				if myVal.strip() == '':
					myCrit += 'book.%s %s System.DateTime.MinValue and ' % (myKey, myOperator)
				else:
					myCrit += 'book.%s %s System.DateTime.Parse(\'%s\') and ' % (myKey, myOperator, myVal)
					#print myCrit
			elif myOperator == '==' and myKey not in numericalKeys:
				if myKey in yesNoKeys:
					myCrit += "comp.yesNo(book.%s,\"%s\") and " % (myKey, myVal)
				elif myKey in mangaYesNoKeys:
					myCrit += "comp.mangaYesNo(book.%s,\"%s\") and " % (myKey, myVal)
				else :
					myCrit = myCrit + "comp.equals(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,unicode(myVal))
			elif myOperator == '<' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.less(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.lessEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greater(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greaterEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<>' and myKey not in numericalKeys:
				if myKey in yesNoKeys:
					myCrit += "not comp.yesNo(book.%s,\"%s\") and " % (myKey, myVal)
				elif myKey in mangaYesNoKeys:
					myCrit += "not comp.mangaYesNo(book.%s,\"%s\") and " % (myKey, myVal)
				else :
					myCrit = myCrit + "comp.notEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			else:
				# numerical values in CR are -1 if Null
				if myKey in numericalKeys and str.Trim(myVal) == '':
					myVal = -1
				if myKey in numericalKeys:
					myCrit = myCrit + ("book.%s %s %s and " % (myKey, myOperator, myVal))
				
			
	myCrit = "if globals()['stop_the_Worker'] == False and " + String.rstrip(myCrit, " and") + ":"
	writeCode(myCrit,1,True)

	#writeCode("print 'rule was executed'",2,True)
	writeCode("theLog += (book.Series.encode('utf-8') + ' v' + str(book.Volume) + ' #' + book.Number.encode('utf-8') + ' was touched \\t(%s)\\n')" % unicode(a[0]), 2, True)
	
	# ----------------------------------------------------------------
	# iterate through each of the newValues
	# ----------------------------------------------------------------

	for n in [n for n in newValues if n.strip() <> '']:


		if len(n) > 0:
			n = n.replace('<<','').lstrip()
			theActionString = n
			theActionString = theActionString.replace('\'','`')
			theActionString = theActionString.replace('\\','\\\\')
			writeCode('theActionString = \"%s\"' % theActionString, 2, True)
			str.lower(n).replace('.setvalue','')		# SetValue is default
			
			# -------------------------------------------------
			# split key and value part of action
			# -------------------------------------------------
			if n.lower().startswith('custom'):		# custom field?
				myCustomField.parseAction(n)
				myKey = myCustomField.theKey
				myModifier = myCustomField.theModifier
				myVal = myCustomField.theVal
			elif String.find(n,':') > 0:			# any other field?
				# get key part (substring before ':')
				tmp = n.split(":",1)
				myKey = tmp[0]
				myModifier = ''
				if String.find(myKey,'.') > 0:
					tmp3 = myKey.split('.')
					myKey = tmp3[0]
					myModifier = tmp3[1]
					myVal = tmp[1]
					
			else:									# no colon (:) in action part? raise syntax error
				File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (missing \':\' after \'%s\')\nline: %s)" % (myKey, s))			
				return 0
			
			# ------------------------------------------------------------
			# store the old value for later use in log file
			# ------------------------------------------------------------
			if myKey.lower().startswith('custom'):
				myCustomKey = myCustomField.customFieldName(myKey)
				writeCode('myOldVal = unicode(book.GetCustomValue(\'%s\'))' % myCustomKey, 2, True)
			else:
				writeCode("myOldVal = unicode(book.%s)" % myKey, 2, True)	# to catch non-ASCII characters

			# ComicRack stores NullValues for numerical fields as -1
			try:
				if myKey in numericalKeys and str(myVal).strip() == '': myVal = -1
			except Exception, err:
				pass
			
			
			if str.lower(myModifier) == 'setvalue':
				myModifier = ''

			writeCode('try:',2,True)
			if myKey.lower().startswith('custom'):
				myKeyName = myCustomField.customFieldName(myKey)
				myVal = myParser.getField(myVal)
				if not myVal.startswith('book.'):
					myVal = '\'%s\'' % myVal
				theAction = 'book.SetCustomValue(\'%s\',str(%s))' % (myKeyName,myVal)
			elif myModifier <> "":
				if str.lower(myModifier) == "calc":
					
					if myKey not in numericalKeys and myKey not in pseudoNumericalKeys:	# <> 'Number':
						myVal = myParser.parseCalc(myVal, str)
					else:
						myVal = myParser.parseCalc(myVal, int)
					if myKey in pseudoNumericalKeys:	# == 'Number':
						theAction = "book.%s = str(%s)" % (myKey, myVal)
					else:
						theAction = "book.%s = %s" % (myKey, myVal)
						
				if str.lower(myModifier) == "add":
					if myKey in multiValueKeys:
						theAction = 'book.%s = multiValue.add(book.%s,"%s", book)' % (myKey, myKey, myVal)
					else: 
						theAction = 'book.%s = dmString.add(book.%s,"%s",book)' %  (myKey, myKey, myVal)

				if str.lower(myModifier) == "replace":
					tmpVal = myVal.split(',')
					if myKey in multiValueKeys:
						theAction = 'book.%s = multiValue.replace(book.%s,"%s","%s", book)' % (myKey, myKey, tmpVal[0], tmpVal[1])
					else:
						'book.%s = dmString.replace(book.%s,"%s","%s",book)' % (myKey, myKey, tmpVal[0], tmpVal[1])
							
				if str.lower(myModifier) == "remove":
					if myKey in multiValueKeys:
						theAction = 'book.%s = multiValue.remove(book.%s,"%s\",book)' % (myKey, myKey, myVal)
					else:
						theAction = 'book.%s = dmString.remove(book.%s,"%s", book)' % (myKey, myKey, myVal)
				if myModifier.lower() == 'removeleading':
					theAction = 'book.%s = dmString.removeLeading(book.%s,"%s", book)' % (myKey, myKey, myVal)

			else:	# myModifier == 'SetValue'
				if myKey in dateTimeKeys:
					theAction = 'book.%s = dmDateTime.setValue(book.%s,"%s", book)' % (myKey, myKey, myVal)
				elif myKey in numericalKeys:
					theAction = 'book.%s = dmNumeric.setValue(book.%s,"%s", book)' % (myKey, myKey, myVal)
				elif myKey in yesNoKeys:
					theAction = 'book.%s = dmYesNo.setValue(book.%s,"%s",book)' % (myKey, myKey, myVal)
				elif myKey in mangaYesNoKeys:
					theAction = 'book.%s = dmMangaYesNo.setValue(book.%s,"%s",book)' % (myKey, myKey, myVal)
				else:
					theAction = 'book.%s = dmString.setValue("%s",book)\n' % (myKey, myVal)
			writeCode('if globals()["stop_the_Worker"] == False:',3,True)
			writeCode	(theAction, 4, True)
			myNewVal = myNewVal + ("\t\tbook.%s = unicode(\"%s\")" % (myKey, myVal)) 

			writeCode('except Exception, err:',2,True)
			writeCode	('ERRCOUNT += 1',3,True)
			writeCode	('if ERRCOUNT == 1:',3,True)
			writeCode		('userIni.write("LastScanErrors",str(ERRCOUNT))',4,True)
			writeCode	('theLog += writeError(f,str(err),theActionString) + "\\n"',3,True)
			writeCode	("if breakAfterFirstError == 'True':",3,True)
			writeCode		("globals()['stop_the_Worker'] = True",4,True)
			writeCode		('theLog += ("Data Manager stopped after first error.\\n")',4,True)

			# this raised an error (issue 80) when used without unicode():
			if myKey.lower().startswith('custom'):
				myCustomKey = myCustomField.customFieldName(myKey)
				writeCode('myNewVal = unicode(book.GetCustomValue(\'%s\'))' % myCustomKey, 2, True)
			else:
				writeCode("myNewVal = unicode(book.%s)" % myKey, 2, True)

			writeCode("if myNewVal <> myOldVal:", 2, True)	
			writeCode	("theLog += ('\\tbook.%s - old value: ' + myOldVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode	("theLog += ('\\tbook.%s - new value: ' + myNewVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode	("book.SetCustomValue(\'DataManager.processed\',strftime(\'%Y-%m-%d\', localtime()))", 3, True)
			
			writeCode("else: pass", 2, True)
			#writeCode	("pass",3,True)

	return -1
	

def writeCode(s, level, linebreak = True):
	''' 
	writes code to dataMan.tmp
	parameters: 
	s - string to write (str)
	level - indentation level (int)
	linebreak - add linebreak? (bool)
	'''

	try:
		s = unicode(s)      # this shouldn't raise an Exception if non-ASCII character is included
	except Exception, err:
		MessageBox.Show(str(err))

	prefix = '\t' * level
	s = prefix + s
	if linebreak == True: s += '\n'
	globalvars.THECODE.append(s)
	return

