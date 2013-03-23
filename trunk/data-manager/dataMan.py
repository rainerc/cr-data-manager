'''
replaceData

plugin script for ComicRack to replace field content in the library
based on user-defined conditions
the rules are read from file replaceData.dat, located in the script directory

The CR Data Manager plugin is licensed under the Apache 2.0 software
license, available at: http://www.apache.org/licenses/LICENSE-2.0.html

v 0.1.11

by docdoom

revision history

v 0.1.11 changes
function writeDataFile() rewritten to make it easier to read with Notepad etc.

>> revision history for older releases is at http://code.google.com/p/cr-replace-data/wiki/RevisionLog

issues:
exclude duplicate lines from parsing
marker in books if handled by the dataman (tags or notes?)
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
IMAGE = Path.Combine(FOLDER, 'dataMan.png')
DONATE = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UQ7JZY366R85S'
WIKI = 'http://code.google.com/p/cr-data-manager/'
MANUAL = 'http://code.google.com/p/cr-data-manager/downloads/list'
VERSION = '0.1.11'

sys.path.append(FOLDER)

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
	'Count',
	'FilePath',
	'FileName',
	'Genre'
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
	'Count',
	'Genre'
	]


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
	if linebreak == True:
		s = s + '\n'
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
	
	# read a line from replaceData.dat and generate python code from it
	
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
				myVal = "%d, %d" % (float(tmp[0]), float(tmp[1]) + 1)
				if myKey in numericalKeys:
					myCrit = myCrit + ("book.%s %s (%s) and " % (myKey, myOperator, myVal))
				else:
					myCrit = myCrit + ("float(book.%s) %s (%s) and " % (myKey, myOperator, myVal))
				print myCrit
			elif myOperator in ('==', '>', '>=', '<', '<=') and myKey == 'Number':
				myCrit = myCrit + ('float(book.%s) %s float(%s) and ' % (myKey, myOperator, myVal))
			elif myModifier == "Contains" and myKey not in numericalKeys:
				myCrit = myCrit + ("String.find(book.%s,\"%s\") >= 0 and " % (myKey,myVal)) 
			elif myModifier == "StartsWith" and myKey not in numericalKeys:
				myCrit = myCrit + ("book.%s.startswith(\"%s\") and " % (myKey,myVal))
				
			else:
				myCrit = myCrit + ("str(book.%s) %s \"%s\" and " % (myKey, myOperator, myVal))
			
	myCrit = "if " + String.rstrip(myCrit, " and") + ":"
	writeCode(myCrit,1,True)
	writeCode("f.write(book.Series.encode('utf-8') + ' v' + str(book.Volume) + ' #' + book.Number + ' was touched\\n')", 2, True)
	
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
			
			writeCode("myOldVal = str(book.%s)" % myKey, 2, True)

			if myModifier <> "":
				if myModifier == "Calc":
					if myKey not in numericalKeys and myKey <> 'Number':
						myVal = String.replace(myVal,'{','str(book.')
					else:
						myVal = String.replace(myVal,'{','int(book.')
					myVal = String.replace(myVal,'}',')')
					if myKey == 'Number':
						writeCode("book.%s = str(%s)" % (myKey, myVal), 2, True)
					else:
						writeCode("book.%s = %s" % (myKey, myVal), 2, True)
			else:
				if myKey in numericalKeys:
					writeCode("book.%s = %s\n" % (myKey, myVal), 2, True)
				else:
					writeCode("book.%s = \"%s\"" % (myKey, myVal), 2, True)
				myNewVal = myNewVal + ("\t\tbook.%s = \"%s\"" % (myKey, myVal)) 

			writeCode("myNewVal = str(book.%s)" % myKey, 2, True)
			writeCode("if myNewVal <> myOldVal:", 2, True)	
			writeCode("f.write('\\tbook.%s - old value: ' + myOldVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode("f.write('\\tbook.%s - new value: ' + myNewVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode("else:", 2, True)
			writeCode("f.write('\\t%s - old value was same as new value\\n')" % (myKey), 3, True)
	return -1
	
def validate(s):
	s = str.Trim(s)
	if not len(s) > 0:
		return ''
	p = re.compile('(<{2}|#)+.*')
	m = p.search(s)
	if m:
		pos = m.start()
	else:
		pos= -1
	if s [0] <> '#':
		if str.count(s, '=>') <> 1:
			return '# invalid expression: %s' % s
		if str.count(s, '<<') <> str.count(s, '>>'):
			return '# invalid expression: %s' % s
		if pos > 0:
			return s [pos:]
	if s[0] == '#' or s[0:2] == '<<':
		return s
	else:
		return '# invalid expression: %s' % s


def writeDataFile(theFile, theText):
	print theText
	s = str.split(str(theText),'\n')
	tmp = str('')
	for line in s:
		s2 = validate(str(line))
		if s2 <> '':
			# using System.Environment.NewLine instead of '\n'
			# to make the file easier to edit with external tool like Notepad
			tmp += validate(str(line)) + System.Environment.NewLine
	if len(theText) > 0:
		File.WriteAllText(theFile, tmp)
	else:
		MessageBox.Show('File not written (0 Byte size)')
	return

def readDataFile(theFile):
	s=[]
	if theFile == DATFILE:
		if File.Exists(DATFILE):
			File.Copy(DATFILE, BAKFILE, True) # just in case something bad happens
			s = File.ReadAllLines(DATFILE)
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
	if len(s) == 0 and theFile == LOGFILE:
		tmp = 'Your criteria matched no book. No data was touched by the Data Manager.'
	return tmp

class displayResults(Form):

	def __init__(self):
		self.Width = 230
		self.Height = 140
		self.StartPosition = FormStartPosition.CenterScreen
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.Text = 'CR Data Manager %s' % VERSION

		self.label = Label()
		self.label.Location = Point(10, 20)
		self.label.Width = 250
		self.label.Height = 30

		self.buttonYes = Button()
		self.buttonYes.Location = Point(10,70)
		self.buttonYes.Text = 'Yes'
		self.buttonYes.DialogResult = DialogResult.Yes

		self.buttonNo = Button()
		self.buttonNo.Location = Point(130,70)
		self.buttonNo.Text = 'No'
		self.buttonNo.DialogResult = DialogResult.No

		self.Controls.Add(self.label)
		self.Controls.Add(self.buttonYes)
		self.Controls.Add(self.buttonNo)

	def configure(self, label):
		self.label.Text = label
		
class progressForm(Form):

	def __init__(self):
		self.Width = 350
		self.Height = 80
		self.StartPosition = FormStartPosition.CenterScreen
		self.Icon = Icon(ICON_SMALL)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.Text = 'CR Data Manager Version %s' % VERSION

		self.progressBar = System.Windows.Forms.ProgressBar()
		self.progressBar.Location = Point(10,10)
		self.progressBar.Width = 330
		self.progressBar.Minimum = 0
		self.progressBar.Step = 1
		
		self.Controls.Add(self.progressBar)

	def setValue(self, s):
		self.progressBar.Value = s

	def setMax(self, s):
		self.progressBar.Maximum = s

class aboutForm(Form):
	
	def __init__(self):
		self.Width = 380
		self.Height = 250
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = True
		self.Text = 'CR Data Manager %s' % VERSION

		self.label = Label()
		self.label.Location = Point(90, 20)
		self.label.Width = 280
		self.label.Height = 110
		self.label.Text = ('The CR Data Manager plugin is licensed under the Apache 2.0 software ' +
			'license, available at:\nhttp://www.apache.org/licenses/LICENSE-2.0.html\n\n' +
			'Big thanks go to 600WPMPO and Casublett: without ' + 
			'their help the plugin would not work as it does now.\n\nImportant links:')

		self.linklabelManual = LinkLabel()
		self.linklabelManual.Location = Point(90,135)
		self.linklabelManual.Text = 'Manual'
		self.linklabelManual.LinkClicked += self.manual

		self.linklabelWiki = LinkLabel()
		self.linklabelWiki.Location = Point(90,155)
		self.linklabelWiki.Text = 'Wiki'
		self.linklabelWiki.LinkClicked += self.wiki

		self.linklabelDonation = LinkLabel()
		self.linklabelDonation.Location = Point(90,175)
		self.linklabelDonation.Text = 'Donations'
		self.linklabelDonation.LinkClicked += self.donate	
			
		self.picturebox = PictureBox()
		self.picturebox.Location = Point(10,10)
		self.picturebox.Image = System.Drawing.Image.FromFile(IMAGE)
		self.picturebox.Height = 70
		self.picturebox.Width = 70
		self.picturebox.SizeMode = PictureBoxSizeMode.StretchImage
		
		self.buttonClose = Button()
		self.buttonClose.Location = Point(290,200)
		self.buttonClose.Text = 'Close'
		self.buttonClose.DialogResult = DialogResult.Cancel
		self.Controls.Add(self.picturebox)
		self.Controls.Add(self.buttonClose)
		self.Controls.Add(self.label)
		self.Controls.Add(self.linklabelDonation)
		self.Controls.Add(self.linklabelManual)
		self.Controls.Add(self.linklabelWiki)

	def donate(self, sender, event):
		System.Diagnostics.Process.Start(DONATE)

	def manual(self, sender, event):
		System.Diagnostics.Process.Start(MANUAL)

	def wiki(self, sender, event):
		System.Diagnostics.Process.Start(WIKI)
		pass
		
class mainForm(Form):

	def __init__(self):
		self.Width = 285
		self.Height = 150
		self.MaximizeBox = False
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = True
		self.Icon = Icon(ICON_SMALL)
		self.Text = 'CR Data Manager %s' % VERSION
		
		self.label = Label()
		self.label.Location = Point(90,20)
		self.label.Text = 'Welcome to the Data Manager.\n\nClick on the icon for more information.'
		self.label.Width = 300
		self.label.Height = 50

		self.picturebox = PictureBox()
		self.picturebox.Location = Point(10,10)
		self.picturebox.Image = System.Drawing.Image.FromFile(IMAGE)
		self.picturebox.Height = 70
		self.picturebox.Width = 70
		self.picturebox.SizeMode = PictureBoxSizeMode.StretchImage
		self.picturebox.Cursor = Cursors.Hand
		self.picturebox.Click += self.aboutDialog
		
		self.tooltip1 = ToolTip()
		self.tooltip1.AutoPopDelay = 5000
		self.tooltip1.InitialDelay = 1000
		self.tooltip1.ShowAlways = True 
		self.tooltip1.SetToolTip(self.picturebox, "click on the image for more information")
		
		self.buttonRun = Button()
		self.buttonRun.Location = Point(10,90)
		self.buttonRun.Width = 120
		self.buttonRun.Text = 'Run the DataMan'
		self.buttonRun.DialogResult = DialogResult.OK

		self.buttonConfig = Button()
		self.buttonConfig.Location = Point(150,90)
		self.buttonConfig.Width = 120
		self.buttonConfig.Text = 'Configure'
		self.buttonConfig.DialogResult = DialogResult.No

		self.Controls.Add(self.label)
		self.Controls.Add(self.buttonRun)
		self.Controls.Add(self.buttonConfig)
		self.Controls.Add(self.picturebox)
		
	def aboutDialog(self, sender, event):
		form = aboutForm()
		form.ShowDialog()
		form.Dispose()
		


class SimpleTextBoxForm(Form):
	
	def __init__(self):

		self.isDirty = False

		self.theFile = ''

		self.Width = 800
		self.Height = 600
		self.MaximizeBox = False
		self.ShowIcon = True
		self.Icon = Icon(ICON_SMALL)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.Closing += self.formClosing
		
		self.textbox = TextBox()
		self.textbox.Location = Point(10, 10)
		self.textbox.Width = 780
		self.textbox.Height = 530
		self.textbox.Multiline = True
		self.textbox.ScrollBars = ScrollBars.Both
		self.textbox.WordWrap = False
		self.textbox.AcceptsTab = True
		self.textbox.TabStop = False

		self.statusLabel = Label()
		self.statusLabel.Location = Point(10,545)
						
		self.button1 = Button()
		self.button1.Text = 'Save'
		self.button1.Location = Point(580, 545)
		self.button1.Width = 100
		self.button1.Click += self.update

		self.button2 = Button()
		self.button2.Text = 'Close'
		self.button2.Width = 100
		self.button2.Location = Point(690, 545)

		self.button2.DialogResult = DialogResult.Cancel
		self.button2.Click += self.reset

		self.Controls.Add(self.textbox)
		self.Controls.Add(self.statusLabel)

		self.addButtons()
		self.showTheFile()
		self.StartPosition = FormStartPosition.CenterParent

	def statusText(self, s):
		if self.theFile == DATFILE:
			self.statusLabel.Text = s

	def update(self, sender, event):
		writeDataFile(DATFILE,self.textbox.Text)
		self.isDirty = False
		self.statusText('data saved')

	def formClosing(self, sender, event):
		if self.isDirty and self.theFile == DATFILE:
			result = (MessageBox.Show(
                   'Would you like to save your changes before closing?'
                   , 'CR Data Manager - %s' % VERSION
                   , MessageBoxButtons.YesNoCancel
                   , MessageBoxIcon.Question))
			if result == DialogResult.Yes:
				if self.theFile == DATFILE:
					writeDataFile(DATFILE,self.textbox.Text)
					self.statusText('')

			elif result == DialogResult.No:
				pass
			elif result == DialogResult.Cancel:
				event.Cancel = True
	
	def textChanged(self, sender, event):
		self.isDirty = True
		self.statusText('* data changed')
		
	def showTheFile(self):
		self.textbox.Text = readDataFile(self.theFile)

	def addButtons(self):
		if self.theFile == DATFILE:
			self.Controls.Add(self.button1)
			self.button2.TabStop = False
			
		self.Controls.Add(self.button2)

	def setFile(self, f):
		self.theFile = f
		self.showTheFile()
		self.textbox.TextChanged += self.textChanged
		self.addButtons()

	def setTitle(self, s):
		self.Text = '%s - Version %s' % (s, VERSION)
		
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

	form = mainForm()
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

	
	writeCode('try:', 0, True)
	
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

	writeCode('except Exception,err:', 0, True)
	writeCode('print (\"Error in code generation: %s\" % str(err))', 1, True)
	
	if ERROR_LEVEL == 0:
		theCode = parsedCode()	# read generated code from file
		print "code generated by CR Data Manager: \n%s" % theCode   # remove in first stable release!
	
		progBar = progressForm()
		progBar.Show()
		progBar.setMax(books.Length)
		touched = 0
		f=open(LOGFILE, "w")	# open logfile
		for book in books:
			touched += 1
			progBar.setValue(touched)
			exec (theCode)
		f.close()				# close logfile

		msg = "Finished. I've inspected %d books.\nDo you want to take look at the log file?" % (touched)

		form = displayResults()
		form.configure(msg)
		form.ShowDialog()
		form.Dispose()

		progBar.Dispose()

		if form.DialogResult == DialogResult.Yes:

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


