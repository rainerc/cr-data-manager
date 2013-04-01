import clr
import System
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *
from System.Drawing import *
from System.IO import File

import globalvars
import utils
#from globalvars import DATFILE, ICON_SMALL, VERSION
from utils import readDataFile, writeDataFile

class configuratorForm(Form):
	
	def __init__(self):

		self.isDirty = False

		self.theFile = ''

		self.Width = 800
		self.Height = 600
		self.MaximizeBox = False
		self.ShowIcon = True
		self.Icon = Icon(globalvars.ICON_SMALL)
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
		self.textbox.Click += self.textBoxClick
		self.textbox.KeyPress += self.textBoxClick
		self.textbox.KeyDown += self.textBoxClick
		
		self.statusLabel = Label()
		self.statusLabel.Width = 70
		self.statusLabel.Location = Point(100,545)

		self.positionLabel = Label()
		self.positionLabel.Width = 70
		self.positionLabel.Location = Point(10,545)
						
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
		self.Controls.Add(self.positionLabel)

		self.addButtons()
		self.showTheFile()
		self.StartPosition = FormStartPosition.CenterParent

		self.positionText('')

	def textBoxClick (self, sender, event):
		line = self.textbox.GetLineFromCharIndex(self.textbox.SelectionStart) + 1
		self.positionText( '@ line %d' % line)

	def positionText (self, s):
		line = self.textbox.GetLineFromCharIndex(self.textbox.SelectionStart) + 1
		self.positionLabel.Text = '@ line %d' % line

	def statusText(self, s):
		if self.theFile == globalvars.DATFILE:
			self.statusLabel.Text = s

	def update(self, sender, event):
		myCursor = self.Cursor.Current
		self.Cursor = Cursors.WaitCursor
		writeDataFile(globalvars.DATFILE,self.textbox.Text)
		self.isDirty = False
		self.statusText('data saved')
		self.Cursor = myCursor

	def formClosing(self, sender, event):
		if self.isDirty and self.theFile == globalvars.DATFILE:
			result = (MessageBox.Show(
                   'Would you like to save your changes before closing?'
                   , 'CR Data Manager - %s' % globalvars.VERSION
                   , MessageBoxButtons.YesNoCancel
                   , MessageBoxIcon.Question))
			if result == DialogResult.Yes:
				if self.theFile == globalvars.DATFILE:
					writeDataFile(globalvars.DATFILE,self.textbox.Text)
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
		if self.theFile == globalvars.DATFILE:
			self.Controls.Add(self.button1)
			self.button2.TabStop = False
			
		self.Controls.Add(self.button2)

	def setFile(self, f):
		self.theFile = f
		self.showTheFile()
		self.textbox.TextChanged += self.textChanged
		self.addButtons()

	def setTitle(self, s):
		self.Text = '%s - Version %s' % (s, globalvars.VERSION)
		
	def reset(self, sender, event):
		self.Close