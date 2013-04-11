
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
import utils
from utils import readFile
from utils import ruleFile
from utils import parser

rulefile = utils.ruleFile()
#parser = utils.parser()

class configuratorForm(Form):
	def __init__(self):
		self.InitializeComponent()
		self.isDirty = False
		self.theFile = ''
		self.searchLabelText = 'search ...'
		self.textBoxHeight = 500
		self.textBoxMinHeight = 260
		self.textClips = [
			'commentary line',
			'divider',
			'group header',
			'variable',
			'end of rules'
			]
		self.dictTextClips = {
			'commentary line': '# ', 
			'divider': '# %s' % ('-' * 30) , 
			'group header': '#@ GROUP ',
			'variable' : '#@ VAR ',
			'end of rules' : '#@ END_RULES'
		}
		self.rulefile = rulefile
		self.allowedKeys = rulefile.allowedKeys
		self.allowedVals = rulefile.allowedVals
#		self.numericalKeys = rulefile.numericalKeys
		self.allowedKeyModifiers = rulefile.allowedKeyModifiers
		self.allowedValModifiers = rulefile.allowedValModifiers
		
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
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
		self._comboTextClips = System.Windows.Forms.ComboBox()
		self._label1 = System.Windows.Forms.Label()
		self._comboKeyModifiers = System.Windows.Forms.ComboBox()
		self._buttonAddCriteria = System.Windows.Forms.Button()
		self._label2 = System.Windows.Forms.Label()
		self._comboValueFields = System.Windows.Forms.ComboBox()
		self._comboValueModifiers = System.Windows.Forms.ComboBox()
		self._buttonAddValues = System.Windows.Forms.Button()
		self._textBoxCriteria = System.Windows.Forms.TextBox()
		self._textBoxValues = System.Windows.Forms.TextBox()
		self._buttonAddTextClip = System.Windows.Forms.Button()
		self._buttonFind = System.Windows.Forms.ToolStripButton()
		self._comboCriteriaFields = System.Windows.Forms.ComboBox()
		self._buttonAddRule = System.Windows.Forms.Button()
		self._textBoxCompleteCriteria = System.Windows.Forms.TextBox()
		self._textBoxCompleteValues = System.Windows.Forms.TextBox()
		self._textBoxTextClips = System.Windows.Forms.TextBox()
		self._textBoxCompleteRule = System.Windows.Forms.TextBox()
		self._comboGroups = System.Windows.Forms.ToolStripComboBox()
		self._labelComboGroups = System.Windows.Forms.ToolStripLabel()
		self._pictureBoxTrashCriteria = System.Windows.Forms.PictureBox()
		self._pictureBoxTrashValues = System.Windows.Forms.PictureBox()
		self._toolTip1 = System.Windows.Forms.ToolTip(self._components)
		self._statusStrip1.SuspendLayout()
		self._toolStrip1.SuspendLayout()
		self._panelGUI.SuspendLayout()
		self._pictureBoxTrashCriteria.BeginInit()
		self._pictureBoxTrashValues.BeginInit()
		self.SuspendLayout()
		# 
		# textBox1
		# 
		self._textBox1.AcceptsReturn = True
		self._textBox1.AcceptsTab = True
		self._textBox1.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBox1.HideSelection = False
		self._textBox1.Location = System.Drawing.Point(12, 28)
		self._textBox1.Multiline = True
		self._textBox1.Name = "textBox1"
		self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
		self._textBox1.Size = System.Drawing.Size(760, 260)
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
			self._buttonFind,
			self._labelComboGroups,
			self._comboGroups]))
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
		self._panelGUI.Controls.Add(self._pictureBoxTrashValues)
		self._panelGUI.Controls.Add(self._pictureBoxTrashCriteria)
		self._panelGUI.Controls.Add(self._textBoxCompleteRule)
		self._panelGUI.Controls.Add(self._textBoxTextClips)
		self._panelGUI.Controls.Add(self._textBoxCompleteValues)
		self._panelGUI.Controls.Add(self._textBoxCompleteCriteria)
		self._panelGUI.Controls.Add(self._buttonAddRule)
		self._panelGUI.Controls.Add(self._comboCriteriaFields)
		self._panelGUI.Controls.Add(self._buttonAddTextClip)
		self._panelGUI.Controls.Add(self._textBoxValues)
		self._panelGUI.Controls.Add(self._textBoxCriteria)
		self._panelGUI.Controls.Add(self._label3)
		self._panelGUI.Controls.Add(self._comboTextClips)
		self._panelGUI.Controls.Add(self._label1)
		self._panelGUI.Controls.Add(self._comboKeyModifiers)
		self._panelGUI.Controls.Add(self._buttonAddCriteria)
		self._panelGUI.Controls.Add(self._label2)
		self._panelGUI.Controls.Add(self._comboValueFields)
		self._panelGUI.Controls.Add(self._comboValueModifiers)
		self._panelGUI.Controls.Add(self._buttonAddValues)
		self._panelGUI.Location = System.Drawing.Point(13, 294)
		self._panelGUI.Name = "panelGUI"
		self._panelGUI.Size = System.Drawing.Size(759, 235)
		self._panelGUI.TabIndex = 22
		self._panelGUI.Visible = False
		self._panelGUI.Paint += self.Panel1Paint
		self._panelGUI.Enter += self.PanelGUIEnter
		# 
		# label3
		# 
		self._label3.AutoSize = True
		self._label3.Location = System.Drawing.Point(13, 174)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(38, 13)
		self._label3.TabIndex = 33
		self._label3.Text = "Others"
		# 
		# comboTextClips
		# 
		self._comboTextClips.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboTextClips.FormattingEnabled = True
		self._comboTextClips.Items.AddRange(System.Array[System.Object](
			["=>",
			"Commentary line",
			"New empty line"]))
		self._comboTextClips.Location = System.Drawing.Point(80, 174)
		self._comboTextClips.Name = "comboTextClips"
		self._comboTextClips.Size = System.Drawing.Size(159, 21)
		self._comboTextClips.TabIndex = 32
		self._comboTextClips.SelectedValueChanged += self.ComboTextClipsSelectedValueChanged
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
		self._comboKeyModifiers.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
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
		self._buttonAddCriteria.Text = "Create"
		self._buttonAddCriteria.UseVisualStyleBackColor = True
		self._buttonAddCriteria.Click += self.ButtonAddCriteriaClick
		# 
		# label2
		# 
		self._label2.AutoSize = True
		self._label2.Location = System.Drawing.Point(13, 68)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(64, 13)
		self._label2.TabIndex = 27
		self._label2.Text = "New Values"
		# 
		# comboValueFields
		# 
		self._comboValueFields.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboValueFields.FormattingEnabled = True
		self._comboValueFields.Location = System.Drawing.Point(80, 68)
		self._comboValueFields.Name = "comboValueFields"
		self._comboValueFields.Size = System.Drawing.Size(159, 21)
		self._comboValueFields.TabIndex = 28
		self._comboValueFields.SelectedIndexChanged += self.ComboValueFieldsSelectedIndexChanged
		# 
		# comboValueModifiers
		# 
		self._comboValueModifiers.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboValueModifiers.FormattingEnabled = True
		self._comboValueModifiers.Location = System.Drawing.Point(246, 68)
		self._comboValueModifiers.Name = "comboValueModifiers"
		self._comboValueModifiers.Size = System.Drawing.Size(121, 21)
		self._comboValueModifiers.TabIndex = 29
		# 
		# buttonAddValues
		# 
		self._buttonAddValues.Location = System.Drawing.Point(660, 68)
		self._buttonAddValues.Name = "buttonAddValues"
		self._buttonAddValues.Size = System.Drawing.Size(75, 23)
		self._buttonAddValues.TabIndex = 31
		self._buttonAddValues.Text = "Create"
		self._buttonAddValues.UseVisualStyleBackColor = True
		self._buttonAddValues.Click += self.ButtonAddValuesClick
		# 
		# textBoxCriteria
		# 
		self._textBoxCriteria.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCriteria.Location = System.Drawing.Point(374, 10)
		self._textBoxCriteria.Name = "textBoxCriteria"
		self._textBoxCriteria.Size = System.Drawing.Size(280, 20)
		self._textBoxCriteria.TabIndex = 34
		# 
		# textBoxValues
		# 
		self._textBoxValues.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxValues.Location = System.Drawing.Point(374, 68)
		self._textBoxValues.Name = "textBoxValues"
		self._textBoxValues.Size = System.Drawing.Size(280, 20)
		self._textBoxValues.TabIndex = 35
		# 
		# buttonAddTextClip
		# 
		self._buttonAddTextClip.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._buttonAddTextClip.Location = System.Drawing.Point(660, 174)
		self._buttonAddTextClip.Name = "buttonAddTextClip"
		self._buttonAddTextClip.Size = System.Drawing.Size(75, 23)
		self._buttonAddTextClip.TabIndex = 36
		self._buttonAddTextClip.Text = "Add"
		self._buttonAddTextClip.UseVisualStyleBackColor = True
		self._buttonAddTextClip.Click += self.ButtonAddTextClipClick
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
		self._comboCriteriaFields.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboCriteriaFields.FormattingEnabled = True
		self._comboCriteriaFields.Location = System.Drawing.Point(81, 10)
		self._comboCriteriaFields.Name = "comboCriteriaFields"
		self._comboCriteriaFields.Size = System.Drawing.Size(159, 21)
		self._comboCriteriaFields.TabIndex = 37
		self._comboCriteriaFields.SelectedIndexChanged += self.ComboCriteriaFieldsSelectedIndexChanged
		# 
		# buttonAddRule
		# 
		self._buttonAddRule.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._buttonAddRule.Location = System.Drawing.Point(660, 125)
		self._buttonAddRule.Name = "buttonAddRule"
		self._buttonAddRule.Size = System.Drawing.Size(75, 43)
		self._buttonAddRule.TabIndex = 38
		self._buttonAddRule.Text = "Add Rule"
		self._buttonAddRule.UseVisualStyleBackColor = True
		self._buttonAddRule.Click += self.ButtonAddRuleClick
		# 
		# textBoxCompleteCriteria
		# 
		self._textBoxCompleteCriteria.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCompleteCriteria.Location = System.Drawing.Point(80, 37)
		self._textBoxCompleteCriteria.Name = "textBoxCompleteCriteria"
		self._textBoxCompleteCriteria.Size = System.Drawing.Size(574, 20)
		self._textBoxCompleteCriteria.TabIndex = 39
		self._textBoxCompleteCriteria.TextChanged += self.TextBoxCompleteCriteriaTextChanged
		# 
		# textBoxCompleteValues
		# 
		self._textBoxCompleteValues.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCompleteValues.Location = System.Drawing.Point(80, 98)
		self._textBoxCompleteValues.Name = "textBoxCompleteValues"
		self._textBoxCompleteValues.Size = System.Drawing.Size(574, 20)
		self._textBoxCompleteValues.TabIndex = 40
		self._textBoxCompleteValues.TextChanged += self.TextBoxCompleteValuesTextChanged
		# 
		# textBoxTextClips
		# 
		self._textBoxTextClips.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxTextClips.Location = System.Drawing.Point(263, 174)
		self._textBoxTextClips.Name = "textBoxTextClips"
		self._textBoxTextClips.Size = System.Drawing.Size(391, 20)
		self._textBoxTextClips.TabIndex = 41
		# 
		# textBoxCompleteRule
		# 
		self._textBoxCompleteRule.Enabled = False
		self._textBoxCompleteRule.Location = System.Drawing.Point(80, 127)
		self._textBoxCompleteRule.Multiline = True
		self._textBoxCompleteRule.Name = "textBoxCompleteRule"
		self._textBoxCompleteRule.ReadOnly = True
		self._textBoxCompleteRule.Size = System.Drawing.Size(574, 41)
		self._textBoxCompleteRule.TabIndex = 42
		# 
		# comboGroups
		# 
		self._comboGroups.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboGroups.Name = "comboGroups"
		self._comboGroups.Size = System.Drawing.Size(121, 25)
		self._comboGroups.SelectedIndexChanged += self.ComboGroupsSelectedIndexChanged
		# 
		# labelComboGroups
		# 
		self._labelComboGroups.Name = "labelComboGroups"
		self._labelComboGroups.Padding = System.Windows.Forms.Padding(20, 0, 0, 0)
		self._labelComboGroups.Size = System.Drawing.Size(86, 22)
		self._labelComboGroups.Text = "find group:"
		# 
		# pictureBoxTrashCriteria
		# 
		self._pictureBoxTrashCriteria.InitialImage = None
		self._pictureBoxTrashCriteria.Location = System.Drawing.Point(54, 36)
		self._pictureBoxTrashCriteria.Name = "pictureBoxTrashCriteria"
		self._pictureBoxTrashCriteria.Size = System.Drawing.Size(25, 26)
		self._pictureBoxTrashCriteria.TabIndex = 43
		self._pictureBoxTrashCriteria.TabStop = False
		self._toolTip1.SetToolTip(self._pictureBoxTrashCriteria, "delete")
		self._pictureBoxTrashCriteria.Click += self.PictureBoxTrashCriteriaClick
		# 
		# pictureBoxTrashValues
		# 
		self._pictureBoxTrashValues.InitialImage = None
		self._pictureBoxTrashValues.Location = System.Drawing.Point(54, 98)
		self._pictureBoxTrashValues.Name = "pictureBoxTrashValues"
		self._pictureBoxTrashValues.Size = System.Drawing.Size(25, 26)
		self._pictureBoxTrashValues.TabIndex = 44
		self._pictureBoxTrashValues.TabStop = False
		self._toolTip1.SetToolTip(self._pictureBoxTrashValues, "delete")
		self._pictureBoxTrashValues.Click += self.PictureBoxTrashValuesClick
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
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Form1"
		self.FormClosing += self.ConfiguratorFormFormClosing
		self.Load += self.ConfiguratorFormLoad
		self._statusStrip1.ResumeLayout(False)
		self._statusStrip1.PerformLayout()
		self._toolStrip1.ResumeLayout(False)
		self._toolStrip1.PerformLayout()
		self._panelGUI.ResumeLayout(False)
		self._panelGUI.PerformLayout()
		self._pictureBoxTrashCriteria.EndInit()
		self._pictureBoxTrashValues.EndInit()
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

		i = 0
		return
	
	def findString(self):
		if str.Trim(self._textBoxSearch.Text) == '' or self._textBoxSearch.Text == self.searchLabelText:
			return
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
		self._pictureBoxTrashCriteria.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._pictureBoxTrashValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
#		self._buttonAddCriteria.Image = System.Drawing.Image.FromFile(globalvars.IMAGEADD)
#		self._buttonAddCriteria.Text = ''
#		self._buttonAddValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEADD)
#		self._buttonAddValues.Text = ''
		self._buttonFind.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._comboCriteriaFields.DataSource = sorted(self.allowedKeys)
		self._comboValueFields.DataSource = sorted(self.allowedVals)
		self._comboKeyModifiers.DataSource = sorted(self.allowedKeyModifiers)
		self._comboValueModifiers.DataSource = self.allowedValModifiers
		self._comboTextClips.DataSource = BindingSource(self.dictTextClips, None)
#		self._comboTextClips.DataSource = self.dictTextClips
#		self._comboTextClips.Items.Add("test1","test2")
#		self._comboTextClips.DisplayMember = self.dictTextClips.keys()
#		self._comboTextClips.ValueMember = self.dictTextClips.values()
		self._labelComboGroups.Visible = self.theFile == globalvars.DATFILE
		self._comboGroups.Visible = self.theFile == globalvars.DATFILE
		self.loadGroups()
		

	def loadGroups(self, sortAlpha = False):
		groups = self.rulefile.groupHeaders()
		self._comboGroups.Items.Clear()
		if not sortAlpha:
			for group in groups:
				self._comboGroups.Items.Add(group)

	def ButtonSaveClick(self, sender, e):
		self.writeRuleFile()
		self.loadGroups()

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
#		self._toolStripStatusLabel3.Text = myKey
		self._comboKeyModifiers.DataSource = sorted(rulefile.getAllowedKeyModifiers(myKey))


	def ComboValueFieldsSelectedIndexChanged(self, sender, e):
		myKey = self._comboValueFields.SelectedValue
#		self._toolStripStatusLabel3.Text = myKey
		self._comboValueModifiers.DataSource = rulefile.getAllowedValModifiers(myKey)

	
	def ButtonAddCriteriaClick(self, sender, e):
		theText = '<<%s.%s:%s>> ' % (
			self._comboCriteriaFields.SelectedValue,
			self._comboKeyModifiers.SelectedValue,
			self._textBoxCriteria.Text
			)
		# check if criterion already in rule
		if self._textBoxCompleteCriteria.Text.find(theText) < 0:
			self._textBoxCompleteCriteria.Text += theText
	
	def ButtonAddValuesClick(self, sender, e):
		theText = '<<%s.%s:%s>> ' % (
			self._comboValueFields.SelectedValue,
			self._comboValueModifiers.SelectedValue,
			self._textBoxValues.Text
			)
		# check if setValue already in rule
		if self._textBoxCompleteValues.Text.find(theText) < 0:
			self._textBoxCompleteValues.Text += theText
	
	
	def TextBoxCompleteCriteriaTextChanged(self, sender, e):
		self._textBoxCompleteRule.Text = self._textBoxCompleteCriteria.Text + ' => ' + self._textBoxCompleteValues.Text
	
	def TextBoxCompleteValuesTextChanged(self, sender, e):
		self._textBoxCompleteRule.Text = self._textBoxCompleteCriteria.Text + ' => ' + self._textBoxCompleteValues.Text
	
	
	def ButtonAddRuleClick(self, sender, e):
		# todo: some syntax checking
		
		self.addRuleToRuleSet('%s => %s' % (self._textBoxCompleteCriteria.Text, self._textBoxCompleteValues.Text), False)

	def addRuleToRuleSet(self,theText,overWriteSelection):
		
		parser = utils.parser()
		parser.validate(theText)
		if parser.err == True:
			MessageBox.Show(parser.error)
			return
		
		myPos = self._textBox1.SelectionStart
		myLen = self._textBox1.SelectionLength
		
		if overWriteSelection == False:
			# in which line is the caret?
			line = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
			
			# create list out of textbox content
			tmp = self._textBox1.Text.split(System.Environment.NewLine)
			
			# insert new rule at line + 1
			tmp.insert(line + 1, theText)
			
			# write list back to textbox content
			newline = System.Environment.NewLine
			self._textBox1.Text = newline.join(tmp)
			
			# highlight inserted rule
			self._textBox1.SelectionStart = self._textBox1.GetFirstCharIndexFromLine(line + 1)
			self._textBox1.SelectionLength = len(theText) - 1
			
			self._textBox1.Focus()
			self._textBox1.ScrollToCaret()
			
			self.setLineInfo()
			
			return
			
		else:
#			myPos = self._textBox1.SelectionStart
#			myLen = self._textBox1.SelectionLength
			hash = self._textBox1.Text
			hashlist = list(hash)
			i = myPos
			while i < myPos + (myLen):
				hashlist.pop(myPos)
				i += 1
	
			hashlist.insert(myPos, theText)
			self._textBox1.Text = ''.join(hashlist)
			self._textBox1.SelectionStart = myPos
			self._textBox1.SelectionLength = len(theText)
			
			self._textBox1.SelectionStart = myPos # + self._textBox1.SelectionLength 
			self._textBox1.SelectionLength = len(theText) 
			self._textBox1.Focus()
			self._textBox1.ScrollToCaret()
			
		return
			

	def TextBox1MouseDown(self, sender, e):
#		if e.Button == MouseButtons.Left:
#			stText = self._textBox1.Text
#			self._textBox1.DoDragDrop(self._textBox1.Text, DragDropEffects.Copy)
			
#			self._textBox1.DoDragDrop(self._textBox1.SelectedText, DragDropEffects.Copy or DragDropEffects.Move)
		pass

	def PanelGUIEnter(self, sender, e):
		if self._textBox1.SelectionLength == 0:
			self._textBox1.SelectionLength = 1
	
	def getTextClipValue(self, myKey):
		for key, value in self.dictTextClips.iteritems():
			if key == myKey:
				return value
		return ''

	def ButtonAddTextClipClick(self, sender, e):
		myVal = self._textBoxTextClips.Text
		# check group header
		if myVal.StartsWith('#@ GROUP'):
			groupName = str.lower(str.Replace(myVal,'#@ GROUP',''))
			if str.Trim(groupName) == '':
				MessageBox.Show('Please add a name for the group','Data Manager for ComicRack %s' % globalvars.VERSION)
				return
			else:
				s = self._textBox1.Text.splitlines()
				for line in [line for line in s if str.lower(line) == str.lower(myVal)]:
					MessageBox.Show('Group name is already used','Data Manager for ComicRack %s' % globalvars.VERSION)
					return				 
			
			
		self.addRuleToRuleSet(myVal, False)

	def ComboTextClipsSelectedValueChanged(self, sender, e):
		myVal = self._comboTextClips.SelectedValue
		self._textBoxTextClips.Text = self.getTextClipValue(myVal)
		

	def ComboGroupsSelectedIndexChanged(self, sender, e):
#		MessageBox.Show(str(self._comboGroups.SelectedItem))
		theText = '#@ GROUP %s' % str(self._comboGroups.SelectedItem)
		s = self._textBox1.Text.splitlines()
		myLine = -1
		i = -1
		for line in s:
			i += 1
			if str.lower(line) == str.lower(theText):
				myLine = i
				break
		pos = self._textBox1.GetFirstCharIndexFromLine(i)
		self._textBox1.SelectionStart = pos
		self._textBox1.SelectionLength = len(theText)
		self._textBox1.Focus()
		self._textBox1.ScrollToCaret()
		pass

	def PictureBoxTrashCriteriaClick(self, sender, e):
		self._textBoxCompleteCriteria.Text = ''
		
	def PictureBoxTrashValuesClick(self, sender, e):
		self._textBoxCompleteValues.Text = ''
		

