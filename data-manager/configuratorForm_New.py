
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
import utils
#from globalvars import DATFILE, ICON_SMALL, VERSION
from utils import readDataFile, writeDataFile

class configuratorForm(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._textBox1 = System.Windows.Forms.TextBox()
		self._buttonClose = System.Windows.Forms.Button()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._toolStripStatusLabel1 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStripStatusLabel2 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStrip1 = System.Windows.Forms.ToolStrip()
		self._toolStripLabel1 = System.Windows.Forms.ToolStripLabel()
		self._buttonSave = System.Windows.Forms.Button()
		self._toolStripStatusLabel3 = System.Windows.Forms.ToolStripStatusLabel()
		self._buttonPlus = System.Windows.Forms.Button()
		self._toolStripTextBox1 = System.Windows.Forms.ToolStripTextBox()
		self._toolStripButton1 = System.Windows.Forms.ToolStripButton()
		self._statusStrip1.SuspendLayout()
		self._toolStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# textBox1
		# 
		self._textBox1.AcceptsReturn = True
		self._textBox1.AcceptsTab = True
		self._textBox1.Location = System.Drawing.Point(12, 28)
		self._textBox1.Multiline = True
		self._textBox1.Name = "textBox1"
		self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
		self._textBox1.Size = System.Drawing.Size(760, 501)
		self._textBox1.TabIndex = 0
		self._textBox1.WordWrap = False
		self._textBox1.Click += self.TextBox1Click
		self._textBox1.KeyPress += self.TextBox1KeyPress
		self._textBox1.KeyUp += self.TextBox1KeyUp
		# 
		# buttonClose
		# 
		self._buttonClose.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._buttonClose.Location = System.Drawing.Point(687, 537)
		self._buttonClose.Name = "buttonClose"
		self._buttonClose.Size = System.Drawing.Size(75, 23)
		self._buttonClose.TabIndex = 1
		self._buttonClose.Text = "Close"
		self._buttonClose.UseVisualStyleBackColor = True
		# 
		# statusStrip1
		# 
		self._statusStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._toolStripStatusLabel1,
			self._toolStripStatusLabel2,
			self._toolStripStatusLabel3]))
		self._statusStrip1.Location = System.Drawing.Point(0, 532)
		self._statusStrip1.Name = "statusStrip1"
		self._statusStrip1.Size = System.Drawing.Size(784, 30)
		self._statusStrip1.TabIndex = 2
		self._statusStrip1.Text = "statusStrip1"
		# 
		# toolStripStatusLabel1
		# 
		self._toolStripStatusLabel1.AutoSize = False
		self._toolStripStatusLabel1.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel1.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel1.Name = "toolStripStatusLabel1"
		self._toolStripStatusLabel1.Size = System.Drawing.Size(100, 25)
		self._toolStripStatusLabel1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# toolStripStatusLabel2
		# 
		self._toolStripStatusLabel2.AutoSize = False
		self._toolStripStatusLabel2.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel2.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel2.Name = "toolStripStatusLabel2"
		self._toolStripStatusLabel2.Size = System.Drawing.Size(30, 25)
		# 
		# toolStrip1
		# 
		self._toolStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._toolStripLabel1,
			self._toolStripTextBox1,
			self._toolStripButton1]))
		self._toolStrip1.Location = System.Drawing.Point(0, 0)
		self._toolStrip1.Name = "toolStrip1"
		self._toolStrip1.Size = System.Drawing.Size(784, 25)
		self._toolStrip1.TabIndex = 3
		self._toolStrip1.Text = "toolStrip1"
		# 
		# toolStripLabel1
		# 
		self._toolStripLabel1.Name = "toolStripLabel1"
		self._toolStripLabel1.Size = System.Drawing.Size(44, 22)
		self._toolStripLabel1.Text = "search:"
		# 
		# buttonSave
		# 
		self._buttonSave.Location = System.Drawing.Point(596, 537)
		self._buttonSave.Name = "buttonSave"
		self._buttonSave.Size = System.Drawing.Size(75, 23)
		self._buttonSave.TabIndex = 4
		self._buttonSave.Text = "Save"
		self._buttonSave.UseVisualStyleBackColor = True
		# 
		# toolStripStatusLabel3
		# 
		self._toolStripStatusLabel3.AutoSize = False
		self._toolStripStatusLabel3.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel3.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel3.Name = "toolStripStatusLabel3"
		self._toolStripStatusLabel3.Size = System.Drawing.Size(100, 25)
		# 
		# buttonPlus
		# 
		self._buttonPlus.Location = System.Drawing.Point(249, 537)
		self._buttonPlus.Name = "buttonPlus"
		self._buttonPlus.Size = System.Drawing.Size(75, 23)
		self._buttonPlus.TabIndex = 5
		self._buttonPlus.Text = "+"
		self._buttonPlus.UseVisualStyleBackColor = True
		self._buttonPlus.Click += self.ButtonPlusClick
		# 
		# toolStripTextBox1
		# 
		self._toolStripTextBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
		self._toolStripTextBox1.Name = "toolStripTextBox1"
		self._toolStripTextBox1.Size = System.Drawing.Size(200, 25)
		self._toolStripTextBox1.Leave += self.ToolStripTextBox1Leave
		self._toolStripTextBox1.DoubleClick += self.ToolStripTextBox1DoubleClick
		# 
		# toolStripButton1
		# 
		self._toolStripButton1.AutoSize = False
		self._toolStripButton1.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text
		self._toolStripButton1.Name = "toolStripButton1"
		self._toolStripButton1.Size = System.Drawing.Size(32, 22)
		self._toolStripButton1.Text = "find"
		self._toolStripButton1.Click += self.ToolStripButton1Click
		# 
		# configuratorForm
		# 
		self.ClientSize = System.Drawing.Size(784, 562)
		self.Controls.Add(self._buttonPlus)
		self.Controls.Add(self._buttonSave)
		self.Controls.Add(self._toolStrip1)
		self.Controls.Add(self._buttonClose)
		self.Controls.Add(self._textBox1)
		self.Controls.Add(self._statusStrip1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.MaximizeBox = False
		self.Name = "configuratorForm"
		self.Text = "Form1"
		self._statusStrip1.ResumeLayout(False)
		self._statusStrip1.PerformLayout()
		self._toolStrip1.ResumeLayout(False)
		self._toolStrip1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()
		


	def TextBox1Click(self, sender, e):
		self.setLineInfo()
		
	def setLineInfo(self):
		line = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart) + 1
		self._toolStripStatusLabel1.Text = 'Line %d' % line	

	def TextBox1KeyPress(self, sender, e):
		self.setLineInfo()

	def TextBox1KeyUp(self, sender, e):
		self.setLineInfo()
		
	def statusText(self, s):
		if self.theFile == globalvars.DATFILE:
			self._toolStripStatusLabel3.Text = s

	def ButtonPlusClick(self, sender, e):
		currentLine = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
		self.setLineInfo()
		tmp = self._textBox1.Text.split(System.Environment.NewLine)
		tmp.insert(currentLine + 1,'New line %d' % currentLine)
		self._textBox1.Text = System.Environment.NewLine.join(tmp)
		i = 0
		return
	
	def findString(self):
		myText = self._textBox1.Text
#		MessageBox.Show(self._toolStrip1.Text)
		try:
			pos = myText.find(self._toolStripTextBox1.Text, self._textBox1.SelectionStart)
			if pos > 0:
				self._textBox1.SelectionStart = pos
				self._textBox1.SelectionLength = len(self._toolStripTextBox1.Text)
				self._textBox1.Focus()
			else:
				pos = 0
				self.findString()
		except Exception, err:
			MessageBox.Show('String not found')
		self.setLineInfo()


	def ToolStripTextBox1DoubleClick(self, sender, e):
		self.findString()

	def ToolStripTextBox1Leave(self, sender, e):
		self.findString()
		pass

	def ToolStripButton1Click(self, sender, e):
		self.findString()