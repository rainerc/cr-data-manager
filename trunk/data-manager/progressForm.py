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
		self.stepsPerformed = 0
		self.maxVal = 0
	
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
			writeCode('try:', 0, True)	
			writeCode('import System',1,True)
			writeCode('from System.Windows.Forms import MessageBox',1,True)
			writeCode('from time import localtime, strftime',1,True)
			writeCode('from globalvars import *',1,True)
			writeCode('from dmutils import *',1,True)
			writeCode('comp = comparer()',1,True)

			s = File.ReadAllLines(globalvars.DATFILE)
			self.maxVal = len(s)
			self._progressBar.Maximum = self.maxVal
			self._progressBar.Step = 1
			i = 0
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
								MessageBox.Show("Error in line %d!\n%s" % (i, error_message),"CR Data Manager %s - Parse error" % globalvars.VERSION)
								self.errorLevel = 1
								break
						if line.startswith('#@ END_RULES'):
							break
					except Exception, err:
						pass
				else:
					MessageBox.Show('Cancellation by user.')
					return
				
			#progBar.Dispose()
			writeCode('except Exception,err:', 0, True)
			writeCode('MessageBox.Show (\"Error in code generation: %s\" % str(err))', 1, True)
			self.Close()
				

		# ------------------------------------------------------
		# run the parsed code over the books:
		# ------------------------------------------------------
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
						exec(myCode)

					except Exception, err:
						print str(Exception.args)
						MessageBox.Show('Error while executing the rules. \n%s\nPlease check your rules.' % str(err), 'Data Manager - Version %s' % globalvars.VERSION)
						self.errorLevel = 1
						break
					
				else:
					f.write('\n\nExcecution cancelled by user.')
					break
				
			f.close()				# close logfile
			self.Close()

			

	def BackgroundWorker1ProgressChanged(self, sender, e):
		# progressBar.Value = xxx  did not update the progressBar properly
		# so we use PerformStep()
		self._progressBar.PerformStep()
		if self.theProcess == globalvars.PROCESS_BOOKS:
			self._label1.Text = 'Data Manager worked on %d books' % self.stepsPerformed
		elif self.theProcess == globalvars.PROCESS_CODE:
			self._label1.Text = 'Data Manager parsed %d rules' % self.stepsPerformed


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
	pseudoNumericalKeys = rules.pseudoNumericalKeys
	multiValueKeys = rules.multiValueKeys
	

	myParser = dmutils.parser()
	myParser.validate(s)
	if myParser.err:
		File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (%s)\nline: %s)" % (myParser.error, s))
		return 0
	
	a = s.split("=>")

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


			# todo: checked up here
			
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

			myVal = tmp[1]
			
			if myKey in numericalKeys and myVal <> '' and stringToFloat(myVal) == None:
				File.AppendAllText(globalvars.ERRFILE,"You entered the string value '%s' as a condition for the numerical field '%s'\n" % (myVal, myKey))
				File.AppendAllText(globalvars.ERRFILE,"This is not allowed. Please check your rules.")
				return 0				


			if myOperator == "in range":		# must only be used with numerical keys
				
				tmp = myVal.split(",")
				#val1 = stringToFloat(tmp[0])    # float
				#val1 = nullToZero(val1)         # float or None
				
				val1 = float((nullToZero(stringToFloat(tmp[0]))))
				val2 = float(nullToZero(stringToFloat(tmp[1])))

				if val1 > val2:
					File.AppendAllText(globalvars.ERRFILE,  "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "first value in range expression must be smaller than second value")
					return 0
				
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
						myVal = stringToFloat(nullToZero(myVal))
						myCrit += ("stringToFloat(nullToZero(book.%s)) %s (%s) and " % (myKey, myOperator, myVal))

# this gave false result (issue 71):
#						myVal = nullToZero(stringToFloat(myVal))		
#						myCrit = myCrit + ('nullToZero(stringToFloat(book.%s)) %s %s and ' % (myKey, myOperator, myVal))
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
			elif myModifier.lower() in ('isanyof','notisanyof'):
				if myKey in multiValueKeys:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "IsAnyOf and NotIsAnyOf modifiers cannot be used in %s field" % (myKey))
					return 0
				if myModifier.lower() == 'isanyof':
					myCrit = myCrit + ('comp.isAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal))
				else:
					myCrit = myCrit + ('comp.isAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == False and ' % (myKey, myVal))
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
	
	# ----------------------------------------------------------------
	# iterate through each of the newValues
	# ----------------------------------------------------------------

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
			writeCode("myOldVal = unicode(book.%s)" % myKey, 2, True)	# to catch non-ASCII characters

			if myKey in numericalKeys and stringToFloat(myVal) == None:
				File.AppendAllText(globalvars.ERRFILE,"You wanted to assign the string value '%s' to the numerical field '%s'\n" % (myVal, myKey))
				File.AppendAllText(globalvars.ERRFILE,"This is not allowed. Please check your rules.")
				return 0				

			if str.lower(myModifier) == 'setvalue':
				myModifier = ''
				
			if myModifier <> "":
				if str.lower(myModifier) == "calc":
					if myKey not in numericalKeys and myKey not in pseudoNumericalKeys:	# <> 'Number':
						myVal = String.replace(myVal,'{','(unicode(book.')	# to catch non-ASCII characters
					else:
						myVal = String.replace(myVal,'{','int(stringToFloat(book.')
					myVal = String.replace(myVal,'}','))')
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
						writeCode('book.%s = stringRemove(book.%s,"%s\", COMPARE_CASE_INSENSITIVE)' % (myKey, myKey, myVal), 2, True)
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


# todo: move stringToFloat to utils.py
def stringToFloat(myVal):
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


