
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
import utils
from utils import readFile
from utils import ruleFile

rulefile = utils.ruleFile()

class configuratorForm(Form):
	def __init__(self):
		self.InitializeComponent()
		self.isDirty = False
		self.theFile = ''
		self.searchLabelText = 'search ...'
		self.textBoxHeight = 500
		self.textBoxMinHeight = 333
		
		self.rulefile = rulefile
		self.allowedKeys = rulefile.allowedKeys
		self.allowedVals = rulefile.allowedVals
#		self.numericalKeys = rulefile.numericalKeys
		self.allowedKeyModifiers = rulefile.allowedKeyModifiers
		self.allowedValModifiers = rulefile.allowedValModifiers
	
	def InitializeComponent(self):
		self._textBox1 = System.Windows.Forms.TextBox()
		self._buttonClose = System.Windows.Forms.Button()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._toolStripStatusLabel1 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStripStatusLabel2 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStrip1 = System.Windows.Forms.ToolStrip()
		self._buttonSave = System.Windows.Forms.Button()
		self._toolStripStatusLabel3 = System.Windows.Forms.ToolStripStatusLabel()
		self._buttonPlus = System.Windows.Forms.Button()
		self._textBoxSearch = System.Windows.Forms.ToolStripTextBox()
		self._panelGUI = System.Windows.Forms.Panel()
		self._label3 = System.Windows.Forms.Label()
		self._comboBox7 = System.Windows.Forms.ComboBox()
		self._label1 = System.Windows.Forms.Label()
		self._comboKeyModifiers = System.Windows.Forms.ComboBox()
		self._buttonAddCriteria = System.Windows.Forms.Button()
		self._label2 = System.Windows.Forms.Label()
		self._comboValFields = System.Windows.Forms.ComboBox()
		self._comboValModifiers = System.Windows.Forms.ComboBox()
		self._button2 = System.Windows.Forms.Button()
		self._textBoxCriteria = System.Windows.Forms.TextBox()
		self._textBox3 = System.Windows.Forms.TextBox()
		self._button3 = System.Windows.Forms.Button()
		self._buttonFind = System.Windows.Forms.ToolStripButton()
		self._comboCriteriaFields = System.Windows.Forms.ComboBox()
		self._statusStrip1.SuspendLayout()
		self._toolStrip1.SuspendLayout()
		self._panelGUI.SuspendLayout()
		self.SuspendLayout()
		# 
		# textBox1
		# 
		self._textBox1.AcceptsReturn = True
		self._textBox1.AcceptsTab = True
		self._textBox1.HideSelection = False
		self._textBox1.Location = System.Drawing.Point(12, 28)
		self._textBox1.Multiline = True
		self._textBox1.Name = "textBox1"
		self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
		self._textBox1.Size = System.Drawing.Size(760, 333)
		self._textBox1.TabIndex = 0
		self._textBox1.TabStop = False
		self._textBox1.WordWrap = False
		self._textBox1.Click += self.TextBox1Click
		self._textBox1.KeyPress += self.TextBox1KeyPress
		self._textBox1.KeyUp += self.TextBox1KeyUp
		self._textBox1.MouseDown += self.TextBox1MouseDown
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
			[self._textBoxSearch,
			self._buttonFind]))
		self._toolStrip1.Location = System.Drawing.Point(0, 0)
		self._toolStrip1.Name = "toolStrip1"
		self._toolStrip1.Size = System.Drawing.Size(784, 25)
		self._toolStrip1.TabIndex = 3
		self._toolStrip1.Text = "toolStrip1"
		# 
		# buttonSave
		# 
		self._buttonSave.Location = System.Drawing.Point(596, 537)
		self._buttonSave.Name = "buttonSave"
		self._buttonSave.Size = System.Drawing.Size(75, 23)
		self._buttonSave.TabIndex = 4
		self._buttonSave.Text = "Save"
		self._buttonSave.UseVisualStyleBackColor = True
		self._buttonSave.Click += self.ButtonSaveClick
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
		self._buttonPlus.Location = System.Drawing.Point(333, 537)
		self._buttonPlus.Name = "buttonPlus"
		self._buttonPlus.Size = System.Drawing.Size(75, 23)
		self._buttonPlus.TabIndex = 5
		self._buttonPlus.Text = "GUI"
		self._buttonPlus.UseVisualStyleBackColor = True
		self._buttonPlus.Click += self.ButtonPlusClick
		# 
		# textBoxSearch
		# 
		self._textBoxSearch.ForeColor = System.Drawing.SystemColors.InactiveCaption
		self._textBoxSearch.Name = "textBoxSearch"
		self._textBoxSearch.Size = System.Drawing.Size(200, 25)
		self._textBoxSearch.Text = "search ..."
		self._textBoxSearch.Enter += self.ToolStripTextBox1Enter
		self._textBoxSearch.Leave += self.ToolStripTextBox1Leave
		self._textBoxSearch.KeyDown += self.ToolStripTextBox1KeyDown
		self._textBoxSearch.DoubleClick += self.ToolStripTextBox1DoubleClick
		# 
		# panelGUI
		# 
		self._panelGUI.Controls.Add(self._comboCriteriaFields)
		self._panelGUI.Controls.Add(self._button3)
		self._panelGUI.Controls.Add(self._textBox3)
		self._panelGUI.Controls.Add(self._textBoxCriteria)
		self._panelGUI.Controls.Add(self._label3)
		self._panelGUI.Controls.Add(self._comboBox7)
		self._panelGUI.Controls.Add(self._label1)
		self._panelGUI.Controls.Add(self._comboKeyModifiers)
		self._panelGUI.Controls.Add(self._buttonAddCriteria)
		self._panelGUI.Controls.Add(self._label2)
		self._panelGUI.Controls.Add(self._comboValFields)
		self._panelGUI.Controls.Add(self._comboValModifiers)
		self._panelGUI.Controls.Add(self._button2)
		self._panelGUI.Location = System.Drawing.Point(12, 367)
		self._panelGUI.Name = "panelGUI"
		self._panelGUI.Size = System.Drawing.Size(759, 138)
		self._panelGUI.TabIndex = 22
		self._panelGUI.Visible = False
		self._panelGUI.Paint += self.Panel1Paint
		# 
		# label3
		# 
		self._label3.AutoSize = True
		self._label3.Location = System.Drawing.Point(13, 67)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(38, 13)
		self._label3.TabIndex = 33
		self._label3.Text = "Others"
		# 
		# comboBox7
		# 
		self._comboBox7.FormattingEnabled = True
		self._comboBox7.Items.AddRange(System.Array[System.Object](
			["=>",
			"Commentary line",
			"New empty line"]))
		self._comboBox7.Location = System.Drawing.Point(80, 67)
		self._comboBox7.Name = "comboBox7"
		self._comboBox7.Size = System.Drawing.Size(159, 21)
		self._comboBox7.TabIndex = 32
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(13, 10)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(100, 23)
		self._label1.TabIndex = 25
		self._label1.Text = "Criteria"
		# 
		# comboKeyModifiers
		# 
		self._comboKeyModifiers.FormattingEnabled = True
		self._comboKeyModifiers.Location = System.Drawing.Point(246, 10)
		self._comboKeyModifiers.Name = "comboKeyModifiers"
		self._comboKeyModifiers.Size = System.Drawing.Size(121, 21)
		self._comboKeyModifiers.TabIndex = 23
		# 
		# buttonAddCriteria
		# 
		self._buttonAddCriteria.Location = System.Drawing.Point(660, 10)
		self._buttonAddCriteria.Name = "buttonAddCriteria"
		self._buttonAddCriteria.Size = System.Drawing.Size(75, 23)
		self._buttonAddCriteria.TabIndex = 26
		self._buttonAddCriteria.Text = "Add"
		self._buttonAddCriteria.UseVisualStyleBackColor = True
		self._buttonAddCriteria.Click += self.ButtonAddCriteriaClick
		# 
		# label2
		# 
		self._label2.AutoSize = True
		self._label2.Location = System.Drawing.Point(13, 39)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(64, 13)
		self._label2.TabIndex = 27
		self._label2.Text = "New Values"
		# 
		# comboValFields
		# 
		self._comboValFields.FormattingEnabled = True
		self._comboValFields.Location = System.Drawing.Point(80, 39)
		self._comboValFields.Name = "comboValFields"
		self._comboValFields.Size = System.Drawing.Size(159, 21)
		self._comboValFields.TabIndex = 28
		# 
		# comboValModifiers
		# 
		self._comboValModifiers.FormattingEnabled = True
		self._comboValModifiers.Location = System.Drawing.Point(246, 39)
		self._comboValModifiers.Name = "comboValModifiers"
		self._comboValModifiers.Size = System.Drawing.Size(121, 21)
		self._comboValModifiers.TabIndex = 29
		# 
		# button2
		# 
		self._button2.Location = System.Drawing.Point(660, 39)
		self._button2.Name = "button2"
		self._button2.Size = System.Drawing.Size(75, 23)
		self._button2.TabIndex = 31
		self._button2.Text = "Add"
		self._button2.UseVisualStyleBackColor = True
		# 
		# textBoxCriteria
		# 
		self._textBoxCriteria.Location = System.Drawing.Point(374, 10)
		self._textBoxCriteria.Name = "textBoxCriteria"
		self._textBoxCriteria.Size = System.Drawing.Size(280, 20)
		self._textBoxCriteria.TabIndex = 34
		# 
		# textBox3
		# 
		self._textBox3.Location = System.Drawing.Point(374, 39)
		self._textBox3.Name = "textBox3"
		self._textBox3.Size = System.Drawing.Size(280, 20)
		self._textBox3.TabIndex = 35
		# 
		# button3
		# 
		self._button3.Location = System.Drawing.Point(660, 67)
		self._button3.Name = "button3"
		self._button3.Size = System.Drawing.Size(75, 23)
		self._button3.TabIndex = 36
		self._button3.Text = "Add"
		self._button3.UseVisualStyleBackColor = True
		# 
		# buttonFind
		# 
		self._buttonFind.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text
		self._buttonFind.ImageTransparentColor = System.Drawing.Color.Magenta
		self._buttonFind.Name = "buttonFind"
		self._buttonFind.Size = System.Drawing.Size(34, 22)
		self._buttonFind.Text = "Find"
		self._buttonFind.Click += self.ButtonFindClick
		# 
		# comboCriteriaFields
		# 
		self._comboCriteriaFields.FormattingEnabled = True
		self._comboCriteriaFields.Location = System.Drawing.Point(81, 10)
		self._comboCriteriaFields.Name = "comboCriteriaFields"
		self._comboCriteriaFields.Size = System.Drawing.Size(159, 21)
		self._comboCriteriaFields.TabIndex = 37
		self._comboCriteriaFields.SelectedIndexChanged += self.ComboCriteriaFieldsSelectedIndexChanged
		# 
		# configuratorForm
		# 
		self.ClientSize = System.Drawing.Size(784, 562)
		self.Controls.Add(self._panelGUI)
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
		self.FormClosing += self.ConfiguratorFormFormClosing
		self.Load += self.ConfiguratorFormLoad
		self._statusStrip1.ResumeLayout(False)
		self._statusStrip1.PerformLayout()
		self._toolStrip1.ResumeLayout(False)
		self._toolStrip1.PerformLayout()
		self._panelGUI.ResumeLayout(False)
		self._panelGUI.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()
		


	def TextBox1Click(self, sender, e):
		self.setLineInfo()
		
	def setLineInfo(self):
		line = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
		col = self._textBox1.SelectionStart - self._textBox1.GetFirstCharIndexFromLine(line);
		self._toolStripStatusLabel1.Text = 'Line %d - Col %d' % (line + 1, col + 1)	

	def TextBox1KeyPress(self, sender, e):
		self.setLineInfo()

	def TextBox1KeyUp(self, sender, e):
		self.setLineInfo()
		
	def statusText(self, s):
		if self.theFile == globalvars.DATFILE:
			self._toolStripStatusLabel3.Text = s

	def ButtonPlusClick(self, sender, e):
		currentLine = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
		currentPos = self._textBox1.SelectionStart
		currentLen = self._textBox1.SelectionLength
		self.setLineInfo()

			
		if self._textBox1.Height == self.textBoxHeight:
			self._textBox1.Height = self.textBoxMinHeight
			self._buttonPlus.Text = 'Editor'
			self._panelGUI.Visible = True
		else:
			self._textBox1.Height = self.textBoxHeight
			self._buttonPlus.Text = 'GUI'
			self._panelGUI.Visible = False
		self._textBox1.SelectionStart = currentPos
		self._textBox1.ScrollToCaret()
		self._textBox1.SelectionLength = currentLen
		

				
#		self._textBox1.Text = System.Environment.NewLine.join(tmp)
		i = 0
		return
	
	def findString(self):
		myText = str.lower(self._textBox1.Text)
		try:
			result = True
			pos = myText.find(str.lower(self._textBoxSearch.Text), self._textBox1.SelectionStart + 1)
			self._textBox1.SelectionStart = pos
			self._textBox1.SelectionLength = len(self._textBoxSearch.Text)
			self._textBox1.Focus()
			self._textBox1.ScrollToCaret()
		except Exception, err:
			MessageBox.Show('End of rule set reached: \"%s\" was not found.' % self._textBoxSearch.Text,
				'Data Manager for ComicRack %s' % globalvars.VERSION)
		self.setLineInfo()

	def showTheFile(self):
		if self.theFile <> '':
			if self.theFile == globalvars.DATFILE:
				ruleFile = utils.ruleFile()
				self._textBox1.Text = ruleFile.read()
				if ruleFile.editedByParser:
					self.isDirty = True
					self.statusText('* data changed')
					MessageBox.Show('Your rules contained %d syntax errors. Those were marked with \"# invalid expression\"' % errlines)
	
			else:
				self._buttonPlus.Visible = False						
				self._textBox1.Text = readFile(self.theFile)
				
	def textChanged(self, sender, event):
		self.isDirty = True
		self.statusText('* data changed')
	
	def setFile(self, f):
		self.theFile = f
		self.showTheFile()
		self._textBox1.TextChanged += self.textChanged
		self.setLineInfo()
		if self.theFile <> globalvars.DATFILE:
			self._buttonSave.Visible = False
		return

	# Search textbox events	
	def ToolStripTextBox1DoubleClick(self, sender, e):
		self.findString()

	def ToolStripTextBox1Leave(self, sender, e):
		if self._textBoxSearch.Text == '':
			self._textBoxSearch.ForeColor = System.Drawing.Color.Gray
			self._textBoxSearch.Text = self.searchLabelText
		pass

	# Search button events
	def ToolStripButton1Click(self, sender, e):
		self.findString()

	def ConfiguratorFormLoad(self, sender, e):
		self.Text = 'Data Manager for ComicRack - Version %s' % (globalvars.VERSION)
		self.showTheFile
		self._textBox1.SelectionStart = 1
		self._textBox1.SelectionLength = 0
		self._textBoxSearch.Text = self.searchLabelText
		self._textBox1.Height = self.textBoxHeight
		self._buttonFind.Image = System.Drawing.Image.FromFile(globalvars.IMAGESEARCH)
		self._buttonFind.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._comboCriteriaFields.DataSource = sorted(self.allowedKeys)
		self._comboValFields.DataSource = sorted(self.allowedVals)
		self._comboKeyModifiers.DataSource = sorted(self.allowedKeyModifiers)
		self._comboValModifiers.DataSource = self.allowedValModifiers

	def ButtonSaveClick(self, sender, e):
		self.writeRuleFile()

	def writeRuleFile(self):
		self.Cursor = Cursors.WaitCursor
		rulefile = utils.ruleFile()
		if rulefile.write(self._textBox1.Text) == rulefile.NOERROR:
			self.showTheFile()
			self.isDirty = False
			self.statusText('data saved')
		else:
			# todo: more meaningful error text
			MessageBox.Show('Data could not be saved')
		self.Cursor = Cursors.Default
		if rulefile.editedByParser:
			# todo: more meaningfull error message
			MessageBox.Show('Some rules were invalid! Those rules were marked.')
		return not rulefile.editedByParser

	def ConfiguratorFormFormClosing(self, sender, e):
		if self.isDirty and self.theFile == globalvars.DATFILE:
			result = (MessageBox.Show(
               'Would you like to save your changes before closing?'
               , 'CR Data Manager - %s' % globalvars.VERSION
               , MessageBoxButtons.YesNoCancel
               , MessageBoxIcon.Question))
			if result == DialogResult.Yes:
				if not self.writeRuleFile(): event.Cancel = True
			elif result == DialogResult.No:
				pass
			elif result == DialogResult.Cancel:
				event.Cancel = True

	def ButtonFindClick(self, sender, e):
		self.findString()

	def ToolStripTextBox1Enter(self, sender, e):
		self._textBoxSearch.ForeColor = System.Drawing.Color.Black
		if self._textBoxSearch.Text == self.searchLabelText:
			self._textBoxSearch.Text = ''
		pass

	def ToolStripTextBox1KeyDown(self, sender, e):
		if e.KeyCode == Keys.Enter and self._textBoxSearch.Text <> '':
			self.findString()
			self._textBoxSearch.Focus()
		

	def Panel1Paint(self, sender, e):
		pass

	def ComboCriteriaFieldsSelectedIndexChanged(self, sender, e):
		myKey = self._comboCriteriaFields.SelectedValue
		self._toolStripStatusLabel3.Text = myKey
		self._comboKeyModifiers.DataSource = sorted(rulefile.getAllowedKeyModifiers(myKey))
		pass

	def ButtonAddCriteriaClick(self, sender, e):
		theText = '<<%s.%s:%s>>' % (
			self._comboCriteriaFields.SelectedValue,
			self._comboKeyModifiers.SelectedValue,
			self._textBoxCriteria.Text
			)
			
		MessageBox.Show(theText)
		if True:
			self.addTextToRuleSet(theText)
		pass
	
	def addTextToRuleSet(self,theText):
		myPos = self._textBox1.SelectionStart
		myLen = self._textBox1.SelectionLength
		hash = self._textBox1.Text
		print myPos
		print myLen
		hashlist = list(hash)
		i = myPos
		while i < myPos + (myLen):
			print hashlist[i]
			hashlist.pop(myPos)
			i += 1

		hashlist.insert(myPos, theText)
		self._textBox1.Text = ''.join(hashlist)
		self._textBox1.SelectionStart = myPos
		self._textBox1.SelectionLength = len(theText)

	def TextBox1MouseDown(self, sender, e):
		if e.Button == MouseButtons.Left:
			stText = self._textBox1.Text
			self._textBox1.DoDragDrop(self._textBox1.Text, DragDropEffects.Copy)
		pass