# ------------------------------------------------------
# replaceData
#
# plugin script for ComicRack to replace field content in the library
# based on user-defined conditions
# the rules are read from file replaceData.dat, located in the script directory
#
# v 0.1.5
# by docdoom
#
# revision history
# v 0.1.5 issues
# range modifier is mis-interpreted
#
# v 0.1.4 changes:
# global use of configurator form (in progress)
# added icons
# added hook in toolbar
# added initial form to run or configure
# added LogFile viewer
# 
# v 0.1.4 fixes:
# exception thrown when StarsWith modifier was used with a second criterion
#
# v 0.1.3 changes:
# Format field can be used
# new modifier StartsWith
# AlternateField can be used
# field Count can be used
# field FilePath can be used
# field FileName can be used
# configuration file can be edited from within ComicRack
#
# v 0.1.3 fixes:
# exception if dataman.dat not exists
#
# revision history for older releases is at http://code.google.com/p/cr-replace-data/wiki/RevisionLog
#
# issues:
# todo: save Guid to tags
# todo: case-insensitive comparison of field names
# todo: case-insensitive comparison of modifiers
# todo: modifier Before
# todo: modifier After
# todo: handling of ''-values
#		e.g. <<Format:>>
# todo: use In as modifier in keys
#      e.g. <<Number.In:1,3,8>>
# todo: add RegExp as modifier
# todo: simulation instead of actual replacing of data
# todo: GUI instead of editing replaceData.dat
# todo: rollback function (need GUID per book)
#    NOTE: better use CR's undo feature? 
# ------------------------------------------------------

import clr
import sys
import re
import System
from System import String
from System.IO import File,  Directory, Path, FileInfo, FileStream
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

global FOLDER
global DATFILE

FOLDER = FileInfo(__file__).DirectoryName + "\\"
DATFILE = Path.Combine(FOLDER, 'dataMan.dat')
SAMPLEFILE = Path.Combine(FOLDER, 'dataManSample.dat')
BAKFILE = Path.Combine(FOLDER, 'dataMan.bak')
ERRFILE = Path.Combine(FOLDER, 'dataMan.err')
TMPFILE = Path.Combine(FOLDER, 'dataMan.tmp')
LOGFILE = Path.Combine(FOLDER, 'dataMan.log')
ICON_SMALL = Path.Combine(FOLDER, 'dataMan16.ico')
ICON = Path.Combine(FOLDER, 'dataMan.ico')

VERSION = '0.1.4'

sys.path.append(FOLDER)
#import dmEditorForm

allowedKeys = [
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
	'Count'
	'FilePath',
	'FileName'
	]

numericalKeys = [
	'Volume',
	'Month',
	'Year',
	'Count'
	]
	
allowedVals = [
	'Series',
	'Volume',
	'Imprint',
	'Publisher',
	'Number',
	'SeriesGroup',
	'MainCharacterOrTeam',
	'Format',
	'AlternateSeries',
	'Count'
	]


def writeCode(s):
	s = str(s)
	try:
		File.AppendAllText(TMPFILE, s)
		
	except Exception, err:
		print "Error in function writeCode: ", str(err)

def parsedCode():
	try:
		return File.ReadAllText(TMPFILE)
	except Exception, err:
		print "Error in function parsedCode: ", str(err)
		
def parseString(s):
	
	# read a line from replaceData.dat and generated python code from it
	
	
	myCrit = ''				# this will later contain the left part of the rule
	myNewVal = ''			# this will later contain the new value (right part of rule)
	myModifier = ''			# the modifier (like Contains, Range, Calc etc.)

	
	a = String.split(s,"=>")
	i = len(a[0])
	a[0] = String.Trim(a[0])
	i = len(a[0])
	
	# split the string and retrieve the criteria (left part) and newValues (right part) 
	# store those in lists
	try:		
		criteria = a[0].split(">>")			
		newValues = String.split(a[1],">>")
	except Exception, err:
		return
	
	# iterate through each of the criteria
	for c in criteria:
		i = len(c)
		if len(c) > 2:
			c = String.Trim(String.replace(c,"<<",""))

			tmp = String.split(c,":",1)
			tmp2 = String.split(tmp[0],".",1)
			myKey = tmp2[0]
			try:
				myModifier = tmp2[1]
			except Exception, err:
				myModifier = ""

			if c <> "" and not (myKey in allowedKeys):
				File.AppendAllText(ERRFILE,"Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			myOperator = "=="
			# handling if modifier is appended to field
			# like Volume.Range:1961, 1963
			try:
				if myModifier <> "":
					if myModifier == "Range":
						myOperator = "in range"
					elif myModifier == "Not":
						myOperator = "<>"
					elif myModifier == "Contains":
						myOperator = ""
					elif myModifier == "Greater":
						myOperator = ">"
					elif myModifier == "GreaterEq":
						myOperator = ">="
					elif myModifier == "Less":
						myOperator = "<"
					elif myModifier == "LessEq":
						myOperator = "<="
					elif myModifier == "StartsWith":
						myOperator = "startswith"
					else:
						File.AppendAllText(ERRFILE,"Syntax not valid (invalid modifier %s)\nline: %s)" % (myModifier, s))
						return 0
											
			except Exception, err:
				print "error at parseString: " + str(err)

			myVal = tmp[1]
			myVal = String.replace(myVal,"\"","\\\"")
			
			if myModifier == "Range":
				tmp = String.Split(myVal,",")
				#myVal = "%d, %d" % (int(tmp[0]), int(tmp[1]) + 1)
				myVal = "%d, %d" % (dec(tmp[0]), dec(tmp[1]))
				if myKey in numericalKeys:
					myCrit = myCrit + ("book.%s %s (%s) and " % (myKey, myOperator, myVal))
				else:
					myCrit = myCrit + ("dec(book.%s) %s (%s) and " % (myKey, myOperator, myVal))
				print myCrit
			elif myModifier == "Contains" and myKey not in numericalKeys:
				myCrit = myCrit + ("String.find(book.%s,\"%s\") >= 0 and " % (myKey,myVal)) 
			elif myModifier == "StartsWith" and myKey not in numericalKeys:
				myCrit = myCrit + ("book.%s.startswith(\"%s\") and " % (myKey,myVal))
				
			else:
				myCrit = myCrit + ("str(book.%s) %s \"%s\" and " % (myKey, myOperator, myVal))
			
	myCrit = "if " + String.rstrip(myCrit, " and") + ":\n"
	writeCode("\t%s\n" % myCrit)
	writeCode("\t\tf.write(book.Series + ' v' + str(book.Volume) + ' #' + book.Number + ' was touched\\n')\n")
	
	# iterate through each of the newValues
	for n in newValues:
		i = len(n)
		if len(n) > 2:
			n = String.Trim(String.replace(n,"<<",""))
			tmp = String.split(n,":",1)
			tmp2 = tmp[0]
			myKey = tmp2
			myModifier = ''
			if String.find(tmp2,'.') > 0:
				tmp3 = String.split(tmp2,'.')
				myKey = tmp3[0]
				myModifier = tmp3[1]
						
			if not (myKey in allowedVals):
				File.AppendAllText(ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			# to do: handling if function is appended to field
				
			myVal = tmp[1]
			
			writeCode("\t\tf.write('\\tbook.%s - old value: ' + str(book.%s) + '\\n')\n" % (myKey, myKey))
			if myModifier <> "":
				if myModifier == "Calc":
					if myVal not in numericalKeys:
						myVal = String.replace(myVal,'{','str(book.')
					else:
						myVal = String.replace(myVal,'{','int(book.')
					myVal = String.replace(myVal,'}',')')
					writeCode("\t\tbook.%s = %s\n" % (myKey, myVal))
			else:
				if myKey in numericalKeys:
					writeCode("\t\tbook.%s = %s\n" % (myKey, myVal))
				else:
					writeCode("\t\tbook.%s = \"%s\"\n" % (myKey, myVal))
				myNewVal = myNewVal + ("\t\tbook.%s = \"%s\"" % (myKey, myVal)) 
				
			writeCode("\t\tf.write('\\tbook.%s - new value: ' + str(book.%s) + '\\n')\n" % (myKey, myKey))
			

	return -1
		
def readDataFile(theFile):
	
	s=[]
	if theFile == DATFILE:
		if File.Exists(DATFILE):
			File.Copy(DATFILE, BAKFILE, True) # just in case something bad happens
			s = File.ReadAllLines(DATFILE)
			# MessageBox.Show ('hugo')
		elif File.Exists(SAMPLEFILE):
			s = File.ReadAllLines(SAMPLEFILE)
	else:
		if File.Exists(theFile):
			s = File.ReadAllLines(theFile)
		else:
			return str('')

	tmp = str('')
	for line in s:
		tmp += line + System.Environment.NewLine
	return tmp

class initialForm(Form):

	def __init__(self):
		self.Width = 300
		self.Height = 150
		self.MaximizeBox = False
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = True
		self.Icon = Icon(ICON_SMALL)
		self.Text = 'CR Data Manager Version %s' % VERSION
		self.label = Label()
		self.label.Location = Point(10,10)
		self.label.Text = 'Welcome to the Data Manager.\nRun it or configure?'
		self.label.Width = 300
		self.label.Height = 50

		self.buttonRun = Button()
		self.buttonRun.Location = Point(10,80)
		self.buttonRun.Width = 100
		self.buttonRun.Text = 'Run the DataMan'
		self.buttonRun.DialogResult = DialogResult.OK
		#self.buttonRun.Click += self.update

		self.buttonConfig = Button()
		self.buttonConfig.Location = Point(120,80)
		self.buttonConfig.Width = 100
		self.buttonConfig.Text = 'Configure'
		self.buttonConfig.DialogResult = DialogResult.No

		self.Controls.Add(self.label)
		self.Controls.Add(self.buttonRun)
		self.Controls.Add(self.buttonConfig)

class SimpleTextBoxForm(Form):
	
	def __init__(self):

		self.theFile = ''

		#self.Text = "dataMan configurator Version " + VERSION

		self.Width = 800
		self.Height = 600
		self.MaximizeBox = False

		#self.Icon = ICON_SMALL
		self.ShowIcon = True
		self.Icon = Icon(ICON_SMALL)
		self.textbox = TextBox()
		#self.textbox.Text = readDataFile(DATFILE)
		self.textbox.Location = Point(10, 10)
		self.textbox.Width = 780
		self.textbox.Height = 500
		self.textbox.Multiline = True
		self.textbox.ScrollBars = ScrollBars.Both
				
		self.button1 = Button()
		self.button1.Text = 'Save and exit'
		self.button1.Location = Point(10, 520)
		self.button1.Width = 200
		self.button1.DialogResult = DialogResult.OK
		self.button1.Click += self.update

		self.button2 = Button()
		self.button2.Text = 'Cancel without saving'
		self.button2.Location = Point(250, 520)
		self.button2.Width = 200
		self.button2.DialogResult = DialogResult.Cancel
		self.button2.Click += self.reset

		self.Controls.Add(self.textbox)

		self.addButtons()
		self.showTheFile()
		#if self.theFile == DATFILE:
		#	self.Controls.Add(self.button1)
		#	self.Controls.Add(self.button2)
		self.StartPosition = FormStartPosition.CenterParent

	def showTheFile(self):
		print self.theFile
		self.textbox.Text = readDataFile(self.theFile)

	def addButtons(self):
		if self.theFile == DATFILE:
			self.Controls.Add(self.button1)
			self.Controls.Add(self.button2)

	def setFile(self, f):
		#MessageBox.Show(f)
		self.theFile = f
		self.showTheFile()
		self.addButtons()

	def setTitle(self, s):
		self.Text = '%s - Version %s' % (s, VERSION)
		#self.addTitle()
		
	def update(self, sender, event):
		File.WriteAllText(DATFILE,self.textbox.Text)
		self.Close

	def reset(self, sender, event):
		self.Close

def dmConfig():

	form = SimpleTextBoxForm()
	form.setFile(DATFILE)
	form.setTitle('Data Manager Configurator')
	form.ShowDialog()
	form.Dispose()


#@Name	Data Manager
#@Image dataMan16.png
#@Hook	Books

def replaceData(books):
	
	ERROR_LEVEL = 0

	form = initialForm()
	form.ShowDialog()
	form.Dispose()

	print form.DialogResult

	if form.DialogResult == DialogResult.No:
		dmConfig()
		return
	elif form.DialogResult <> DialogResult.OK:
		return
	else:
		pass
	
	try:
		File.Delete(TMPFILE)
		File.Delete(ERRFILE)
	except Exception, err:
		pass
	
	if not File.Exists(DATFILE):
		MessageBox.Show('Please use the Data Manager Configurator first!','Data Manager %s' % VERSION)
		return

	writeCode('try:\n')
	
	try:
		s = File.ReadAllLines(DATFILE)
		i = 0
		for line in s:
			i += 1
			if String.find(line," => ") and line[0] <> "#":
				if not parseString(line):
					error_message = File.ReadAllText(ERRFILE)
					MessageBox.Show("Error in line %d!\n%s" % (i, str(error_message)),"Parse error")
					ERROR_LEVEL = 1
			
	except Exception, err:
		print 'getCode: ', str(err)

	writeCode('except Exception,err:\n')
	writeCode('\tMessageBox.Show(\"Error in code generation: %s\" % str(err))')
	
	if ERROR_LEVEL == 0:
		theCode = parsedCode()	# read generated code from file
		print "the code: \n%s" % theCode   # remove in first stable release!
	
	
		touched = 0
		f=open(LOGFILE, "w")	# open logfile
		for book in books:
			touched += 1
			exec (theCode)
		f.close()				# close logfile
		msg = "Finished. I've inspected %d books. Do you want to take look at the log file?" % (touched)
		caption = 'CR Data Manager Version %s' % VERSION
		ret = MessageBox.Show(msg, caption, MessageBoxButtons.YesNo, MessageBoxIcon.Question)
		if ret == DialogResult.Yes:
			form = SimpleTextBoxForm()
			form.setFile(LOGFILE)
			form.setTitle('Data Manager Logfile')
			form.ShowDialog()
			form.Dispose()

		try:
			File.Delete(TMPFILE)
			File.Delete(ERRFILE)
		except Exception, err:
			pass


