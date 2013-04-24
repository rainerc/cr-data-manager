
import System.Drawing
import System.Windows.Forms
from System.Windows.Forms import OpenFileDialog, SaveFileDialog

import System.IO
from System.IO import File

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
import utils
from utils import readFile
from utils import ruleFile
from utils import parser

import aboutForm
from aboutForm import aboutForm

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
		self.textBoxWidth = 760
		self.textBoxMinWidth = 717

		self.dictTextClips = {
			'commentary line': '# ', 
			'divider': '# %s' % ('-' * 30) , 
			'group header': '#@ GROUP ',
			'variable' : '#@ VAR ',
			'end of rules' : '#@ END_RULES',
			'end of group' : '#@ END_GROUP	',
			'author' : '#@ AUTHOR ',
			'notes' : '#@ NOTES ',
			'end of notes' : '#@ END_NOTES'
		}
		
		self.EDITOR_MODE_GUI = 0
		self.EDITOR_MODE_TEXT = 1
		self.editormode = self.EDITOR_MODE_GUI
		self.clearValuesAfterAdding = False
		self.rulefile = rulefile
		self.allowedKeys = rulefile.allowedKeys
		self.allowedVals = rulefile.allowedVals
#		self.numericalKeys = rulefile.numericalKeys
		self.allowedKeyModifiers = rulefile.allowedKeyModifiers
		self.allowedValModifiers = rulefile.allowedValModifiers
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Icon = Icon(globalvars.ICON_SMALL)
		
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._textBox1 = System.Windows.Forms.TextBox()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._toolStripStatusLabel1 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStripStatusLabel2 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStrip1 = System.Windows.Forms.ToolStrip()
		self._toolStripStatusLabel3 = System.Windows.Forms.ToolStripStatusLabel()
		self._textBoxSearch = System.Windows.Forms.ToolStripTextBox()
		self._panelGUI = System.Windows.Forms.Panel()
		self._label3 = System.Windows.Forms.Label()
		self._comboTextClips = System.Windows.Forms.ComboBox()
		self._label1 = System.Windows.Forms.Label()
		self._comboKeyModifiers = System.Windows.Forms.ComboBox()
		self._cmdAddCriteria = System.Windows.Forms.Button()
		self._label2 = System.Windows.Forms.Label()
		self._comboValueFields = System.Windows.Forms.ComboBox()
		self._comboValueModifiers = System.Windows.Forms.ComboBox()
		self._cmdAddValues = System.Windows.Forms.Button()
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
		self._toolTip1 = System.Windows.Forms.ToolTip(self._components)
		self._checkBoxClearValuesAfterAdding = System.Windows.Forms.CheckBox()
		self._menuStrip1 = System.Windows.Forms.MenuStrip()
		self._mnuFile = System.Windows.Forms.ToolStripMenuItem()
		self._saveToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._saveAsToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripSeparator1 = System.Windows.Forms.ToolStripSeparator()
		self._closeToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripSeparator2 = System.Windows.Forms.ToolStripSeparator()
		self._restorelStripMenuItem1 = System.Windows.Forms.ToolStripMenuItem()
		self._helpToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._aboutTheDataManagerToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripLabel1 = System.Windows.Forms.ToolStripLabel()
		self._textBoxSelectLine = System.Windows.Forms.ToolStripTextBox()
		self._buttonGotoLine = System.Windows.Forms.ToolStripButton()
		self._cmdLineToGui = System.Windows.Forms.Button()
		self._cmdTrashCriteria = System.Windows.Forms.Button()
		self._cmdTrashValues = System.Windows.Forms.Button()
		self._cmdRemoveLine = System.Windows.Forms.Button()
		self._mnuEdit = System.Windows.Forms.ToolStripMenuItem()
		self._copyCurrentLineToVisualEditorToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._removeCurrentLineToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._mnuView = System.Windows.Forms.ToolStripMenuItem()
		self._mnuTextEditor = System.Windows.Forms.ToolStripMenuItem()
		self._mnuGuiEditor = System.Windows.Forms.ToolStripMenuItem()
		self._statusStrip1.SuspendLayout()
		self._toolStrip1.SuspendLayout()
		self._panelGUI.SuspendLayout()
		self._menuStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# textBox1
		# 
		self._textBox1.AcceptsReturn = True
		self._textBox1.AcceptsTab = True
		self._textBox1.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBox1.HideSelection = False
		self._textBox1.Location = System.Drawing.Point(12, 52)
		self._textBox1.Multiline = True
		self._textBox1.Name = "textBox1"
		self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
		self._textBox1.Size = System.Drawing.Size(722, 260)
		self._textBox1.TabIndex = 0
		self._textBox1.TabStop = False
		self._textBox1.WordWrap = False
		self._textBox1.Click += self.TextBox1Click
		self._textBox1.KeyPress += self.TextBox1KeyPress
		self._textBox1.KeyUp += self.TextBox1KeyUp
		self._textBox1.Leave += self.TextBox1Leave
		self._textBox1.MouseDown += self.TextBox1MouseDown
		# 
		# statusStrip1
		# 
		self._statusStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._toolStripStatusLabel1,
			self._toolStripStatusLabel2,
			self._toolStripStatusLabel3]))
		self._statusStrip1.Location = System.Drawing.Point(0, 569)
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
			self._comboGroups,
			self._toolStripLabel1,
			self._textBoxSelectLine,
			self._buttonGotoLine]))
		self._toolStrip1.Location = System.Drawing.Point(0, 24)
		self._toolStrip1.Name = "toolStrip1"
		self._toolStrip1.Size = System.Drawing.Size(784, 25)
		self._toolStrip1.TabIndex = 3
		self._toolStrip1.Text = "toolStrip1"
		# 
		# toolStripStatusLabel3
		# 
		self._toolStripStatusLabel3.AutoSize = False
		self._toolStripStatusLabel3.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel3.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel3.Name = "toolStripStatusLabel3"
		self._toolStripStatusLabel3.Size = System.Drawing.Size(100, 25)
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
		self._panelGUI.Controls.Add(self._cmdTrashValues)
		self._panelGUI.Controls.Add(self._cmdTrashCriteria)
		self._panelGUI.Controls.Add(self._checkBoxClearValuesAfterAdding)
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
		self._panelGUI.Controls.Add(self._cmdAddCriteria)
		self._panelGUI.Controls.Add(self._label2)
		self._panelGUI.Controls.Add(self._comboValueFields)
		self._panelGUI.Controls.Add(self._comboValueModifiers)
		self._panelGUI.Controls.Add(self._cmdAddValues)
		self._panelGUI.Location = System.Drawing.Point(13, 322)
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
		self._label3.Size = System.Drawing.Size(29, 13)
		self._label3.TabIndex = 33
		self._label3.Text = "Clips"
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
		# cmdAddCriteria
		# 
		self._cmdAddCriteria.Location = System.Drawing.Point(727, 6)
		self._cmdAddCriteria.Name = "cmdAddCriteria"
		self._cmdAddCriteria.Size = System.Drawing.Size(27, 27)
		self._cmdAddCriteria.TabIndex = 26
		self._toolTip1.SetToolTip(self._cmdAddCriteria, "create criteria element")
		self._cmdAddCriteria.UseVisualStyleBackColor = True
		self._cmdAddCriteria.Click += self.ButtonAddCriteriaClick
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
		# cmdAddValues
		# 
		self._cmdAddValues.Location = System.Drawing.Point(727, 65)
		self._cmdAddValues.Name = "cmdAddValues"
		self._cmdAddValues.Size = System.Drawing.Size(27, 27)
		self._cmdAddValues.TabIndex = 31
		self._toolTip1.SetToolTip(self._cmdAddValues, "create new value element")
		self._cmdAddValues.UseVisualStyleBackColor = True
		self._cmdAddValues.Click += self.ButtonAddValuesClick
		# 
		# textBoxCriteria
		# 
		self._textBoxCriteria.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCriteria.Location = System.Drawing.Point(374, 10)
		self._textBoxCriteria.Name = "textBoxCriteria"
		self._textBoxCriteria.Size = System.Drawing.Size(347, 20)
		self._textBoxCriteria.TabIndex = 34
		# 
		# textBoxValues
		# 
		self._textBoxValues.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxValues.Location = System.Drawing.Point(374, 68)
		self._textBoxValues.Name = "textBoxValues"
		self._textBoxValues.Size = System.Drawing.Size(347, 20)
		self._textBoxValues.TabIndex = 35
		# 
		# buttonAddTextClip
		# 
		self._buttonAddTextClip.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._buttonAddTextClip.Location = System.Drawing.Point(660, 174)
		self._buttonAddTextClip.Name = "buttonAddTextClip"
		self._buttonAddTextClip.Size = System.Drawing.Size(94, 23)
		self._buttonAddTextClip.TabIndex = 36
		self._buttonAddTextClip.Text = "Add clip"
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
		self._buttonAddRule.Size = System.Drawing.Size(94, 43)
		self._buttonAddRule.TabIndex = 38
		self._buttonAddRule.Text = "Add Rule"
		self._buttonAddRule.UseVisualStyleBackColor = True
		self._buttonAddRule.Click += self.ButtonAddRuleClick
		# 
		# textBoxCompleteCriteria
		# 
		self._textBoxCompleteCriteria.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCompleteCriteria.Location = System.Drawing.Point(80, 39)
		self._textBoxCompleteCriteria.Name = "textBoxCompleteCriteria"
		self._textBoxCompleteCriteria.Size = System.Drawing.Size(641, 20)
		self._textBoxCompleteCriteria.TabIndex = 39
		self._textBoxCompleteCriteria.TextChanged += self.TextBoxCompleteCriteriaTextChanged
		# 
		# textBoxCompleteValues
		# 
		self._textBoxCompleteValues.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBoxCompleteValues.Location = System.Drawing.Point(80, 98)
		self._textBoxCompleteValues.Name = "textBoxCompleteValues"
		self._textBoxCompleteValues.Size = System.Drawing.Size(641, 20)
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
		self._comboGroups.IntegralHeight = False
		self._comboGroups.MaxDropDownItems = 30
		self._comboGroups.Name = "comboGroups"
		self._comboGroups.Size = System.Drawing.Size(200, 25)
		self._comboGroups.SelectedIndexChanged += self.ComboGroupsSelectedIndexChanged
		# 
		# labelComboGroups
		# 
		self._labelComboGroups.Margin = System.Windows.Forms.Padding(20, 1, 0, 2)
		self._labelComboGroups.Name = "labelComboGroups"
		self._labelComboGroups.Size = System.Drawing.Size(66, 22)
		self._labelComboGroups.Text = "find group:"
		# 
		# checkBoxClearValuesAfterAdding
		# 
		self._checkBoxClearValuesAfterAdding.Location = System.Drawing.Point(13, 206)
		self._checkBoxClearValuesAfterAdding.Name = "checkBoxClearValuesAfterAdding"
		self._checkBoxClearValuesAfterAdding.Size = System.Drawing.Size(185, 24)
		self._checkBoxClearValuesAfterAdding.TabIndex = 47
		self._checkBoxClearValuesAfterAdding.Text = "clear values after adding a rule"
		self._checkBoxClearValuesAfterAdding.UseVisualStyleBackColor = True
		self._checkBoxClearValuesAfterAdding.CheckedChanged += self.CheckBoxClearValuesAfterAddingCheckedChanged
		# 
		# menuStrip1
		# 
		self._menuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._mnuFile,
			self._mnuEdit,
			self._mnuView,
			self._helpToolStripMenuItem]))
		self._menuStrip1.Location = System.Drawing.Point(0, 0)
		self._menuStrip1.Name = "menuStrip1"
		self._menuStrip1.Size = System.Drawing.Size(784, 24)
		self._menuStrip1.TabIndex = 23
		self._menuStrip1.Text = "menuStrip1"
		# 
		# mnuFile
		# 
		self._mnuFile.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._saveToolStripMenuItem,
			self._toolStripSeparator2,
			self._saveAsToolStripMenuItem,
			self._restorelStripMenuItem1,
			self._toolStripSeparator1,
			self._closeToolStripMenuItem]))
		self._mnuFile.Name = "mnuFile"
		self._mnuFile.Size = System.Drawing.Size(37, 20)
		self._mnuFile.Text = "&File"
		# 
		# saveToolStripMenuItem
		# 
		self._saveToolStripMenuItem.Name = "saveToolStripMenuItem"
		self._saveToolStripMenuItem.Size = System.Drawing.Size(167, 22)
		self._saveToolStripMenuItem.Text = "Save"
		self._saveToolStripMenuItem.Click += self.SaveToolStripMenuItemClick
		# 
		# saveAsToolStripMenuItem
		# 
		self._saveAsToolStripMenuItem.Name = "saveAsToolStripMenuItem"
		self._saveAsToolStripMenuItem.Size = System.Drawing.Size(167, 22)
		self._saveAsToolStripMenuItem.Text = "Backup ..."
		self._saveAsToolStripMenuItem.Click += self.SaveAsToolStripMenuItemClick
		# 
		# toolStripSeparator1
		# 
		self._toolStripSeparator1.Name = "toolStripSeparator1"
		self._toolStripSeparator1.Size = System.Drawing.Size(164, 6)
		# 
		# closeToolStripMenuItem
		# 
		self._closeToolStripMenuItem.Name = "closeToolStripMenuItem"
		self._closeToolStripMenuItem.Size = System.Drawing.Size(167, 22)
		self._closeToolStripMenuItem.Text = "Close"
		self._closeToolStripMenuItem.Click += self.CloseToolStripMenuItemClick
		# 
		# toolStripSeparator2
		# 
		self._toolStripSeparator2.Name = "toolStripSeparator2"
		self._toolStripSeparator2.Size = System.Drawing.Size(164, 6)
		# 
		# restorelStripMenuItem1
		# 
		self._restorelStripMenuItem1.Name = "restorelStripMenuItem1"
		self._restorelStripMenuItem1.Size = System.Drawing.Size(167, 22)
		self._restorelStripMenuItem1.Text = "Restore Backup ..."
		self._restorelStripMenuItem1.Click += self.RestorelStripMenuItem1Click
		# 
		# helpToolStripMenuItem
		# 
		self._helpToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._aboutTheDataManagerToolStripMenuItem]))
		self._helpToolStripMenuItem.Name = "helpToolStripMenuItem"
		self._helpToolStripMenuItem.Size = System.Drawing.Size(44, 20)
		self._helpToolStripMenuItem.Text = "&Help"
		# 
		# aboutTheDataManagerToolStripMenuItem
		# 
		self._aboutTheDataManagerToolStripMenuItem.Name = "aboutTheDataManagerToolStripMenuItem"
		self._aboutTheDataManagerToolStripMenuItem.Size = System.Drawing.Size(204, 22)
		self._aboutTheDataManagerToolStripMenuItem.Text = "About the Data Manager"
		self._aboutTheDataManagerToolStripMenuItem.Click += self.AboutTheDataManagerToolStripMenuItemClick
		# 
		# toolStripLabel1
		# 
		self._toolStripLabel1.Margin = System.Windows.Forms.Padding(20, 1, 0, 2)
		self._toolStripLabel1.Name = "toolStripLabel1"
		self._toolStripLabel1.Size = System.Drawing.Size(57, 22)
		self._toolStripLabel1.Text = "goto line:"
		# 
		# textBoxSelectLine
		# 
		self._textBoxSelectLine.Name = "textBoxSelectLine"
		self._textBoxSelectLine.Size = System.Drawing.Size(40, 25)
		# 
		# buttonGotoLine
		# 
		self._buttonGotoLine.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text
		self._buttonGotoLine.ImageTransparentColor = System.Drawing.Color.Magenta
		self._buttonGotoLine.Name = "buttonGotoLine"
		self._buttonGotoLine.Size = System.Drawing.Size(25, 22)
		self._buttonGotoLine.Text = "go"
		self._buttonGotoLine.Click += self.ButtonGotoLineClick
		# 
		# cmdLineToGui
		# 
		self._cmdLineToGui.AutoSize = True
		self._cmdLineToGui.Location = System.Drawing.Point(740, 285)
		self._cmdLineToGui.Name = "cmdLineToGui"
		self._cmdLineToGui.Size = System.Drawing.Size(27, 27)
		self._cmdLineToGui.TabIndex = 47
		self._toolTip1.SetToolTip(self._cmdLineToGui, """copy current line
to visual editor""")
		self._cmdLineToGui.UseVisualStyleBackColor = True
		self._cmdLineToGui.Click += self.CmdLineToGuiClick
		# 
		# cmdTrashCriteria
		# 
		self._cmdTrashCriteria.Location = System.Drawing.Point(727, 34)
		self._cmdTrashCriteria.Name = "cmdTrashCriteria"
		self._cmdTrashCriteria.Size = System.Drawing.Size(27, 27)
		self._cmdTrashCriteria.TabIndex = 49
		self._toolTip1.SetToolTip(self._cmdTrashCriteria, "remove criteria element")
		self._cmdTrashCriteria.UseVisualStyleBackColor = True
		self._cmdTrashCriteria.Click += self.CmdTrashCriteriaClick
		# 
		# cmdTrashValues
		# 
		self._cmdTrashValues.Location = System.Drawing.Point(727, 94)
		self._cmdTrashValues.Name = "cmdTrashValues"
		self._cmdTrashValues.Size = System.Drawing.Size(27, 27)
		self._cmdTrashValues.TabIndex = 50
		self._toolTip1.SetToolTip(self._cmdTrashValues, "remove value element")
		self._cmdTrashValues.UseVisualStyleBackColor = True
		self._cmdTrashValues.Click += self.CmdTrashValuesClick
		# 
		# cmdRemoveLine
		# 
		self._cmdRemoveLine.AutoSize = True
		self._cmdRemoveLine.Location = System.Drawing.Point(740, 255)
		self._cmdRemoveLine.Name = "cmdRemoveLine"
		self._cmdRemoveLine.Size = System.Drawing.Size(27, 27)
		self._cmdRemoveLine.TabIndex = 48
		self._toolTip1.SetToolTip(self._cmdRemoveLine, "remove current line from rule set")
		self._cmdRemoveLine.UseVisualStyleBackColor = True
		self._cmdRemoveLine.Click += self.CmdRemoveLineClick
		# 
		# mnuEdit
		# 
		self._mnuEdit.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._copyCurrentLineToVisualEditorToolStripMenuItem,
			self._removeCurrentLineToolStripMenuItem]))
		self._mnuEdit.Name = "mnuEdit"
		self._mnuEdit.Size = System.Drawing.Size(39, 20)
		self._mnuEdit.Text = "&Edit"
		# 
		# copyCurrentLineToVisualEditorToolStripMenuItem
		# 
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Name = "copyCurrentLineToVisualEditorToolStripMenuItem"
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Size = System.Drawing.Size(246, 22)
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Text = "Copy current line to visual editor"
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Click += self.CmdLineToGuiClick
		# 
		# removeCurrentLineToolStripMenuItem
		# 
		self._removeCurrentLineToolStripMenuItem.Name = "removeCurrentLineToolStripMenuItem"
		self._removeCurrentLineToolStripMenuItem.Size = System.Drawing.Size(246, 22)
		self._removeCurrentLineToolStripMenuItem.Text = "Remove current line"
		# 
		# mnuView
		# 
		self._mnuView.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._mnuTextEditor,
			self._mnuGuiEditor]))
		self._mnuView.Name = "mnuView"
		self._mnuView.Size = System.Drawing.Size(44, 20)
		self._mnuView.Text = "&View"
		# 
		# mnuTextEditor
		# 
		self._mnuTextEditor.Name = "mnuTextEditor"
		self._mnuTextEditor.Size = System.Drawing.Size(148, 22)
		self._mnuTextEditor.Text = "text editor"
		self._mnuTextEditor.Click += self.MnuTextEditorClick
		# 
		# mnuGuiEditor
		# 
		self._mnuGuiEditor.Name = "mnuGuiEditor"
		self._mnuGuiEditor.Size = System.Drawing.Size(148, 22)
		self._mnuGuiEditor.Text = "graphic editor"
		self._mnuGuiEditor.Click += self.MnuGuiEditorClick
		# 
		# configuratorForm
		# 
		self.ClientSize = System.Drawing.Size(784, 599)
		self.Controls.Add(self._textBox1)
		self.Controls.Add(self._panelGUI)
		self.Controls.Add(self._toolStrip1)
		self.Controls.Add(self._statusStrip1)
		self.Controls.Add(self._menuStrip1)
		self.Controls.Add(self._cmdLineToGui)
		self.Controls.Add(self._cmdRemoveLine)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MainMenuStrip = self._menuStrip1
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
		self._menuStrip1.ResumeLayout(False)
		self._menuStrip1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()
		


	def TextBox1Click(self, sender, e):
		self.setLineInfo()
		
	def setLineInfo(self):
		line = self.currentLine()
		col = self._textBox1.SelectionStart - self._textBox1.GetFirstCharIndexFromLine(line);
		self._toolStripStatusLabel1.Text = 'Line %d - Col %d' % (line + 1, col + 1)
		validRule = self.lineContent(line).startswith('<<')
#		MessageBox.Show(str(validRule))
		self._cmdLineToGui.Enabled = validRule
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Enabled = validRule

	def TextBox1KeyPress(self, sender, e):
		self.setLineInfo()

	def TextBox1KeyUp(self, sender, e):
		self.setLineInfo()
		
	def statusText(self, s):
		if self.theFile == globalvars.DATFILE:
			self._toolStripStatusLabel3.Text = s
#
#	def ButtonPlusClick(self, sender, e):
#		currentLine = self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
#		currentPos = self._textBox1.SelectionStart
#		currentLen = self._textBox1.SelectionLength
#		self.setLineInfo()
#		self._textBox1.SelectionStart = currentPos
#		self._textBox1.ScrollToCaret()
#		self._textBox1.SelectionLength = currentLen
#		self.setEditorMode(not self.editormode)

#						
#		if self._textBox1.Height == self.textBoxHeight:
#			self._textBox1.Height = self.textBoxMinHeight
#			self._textBox1.Width = self.textBoxMinWidth
#			self._buttonPlus.Text = 'Editor'
#			self._panelGUI.Visible = True
#		else:
#			self._textBox1.Height = self.textBoxHeight
#			self._textBox1.Width = self.textBoxWidth
#			self._buttonPlus.Text = 'GUI'
#			self._panelGUI.Visible = False


		i = 0
		return
	
	def setEditorMode(self,editormode):
		if editormode == self.EDITOR_MODE_TEXT:
			self._textBox1.Height = self.textBoxHeight
			self._textBox1.Width = self.textBoxWidth
			self._mnuEdit.Enabled = False
			self._panelGUI.Visible = False
			self._mnuTextEditor.Enabled = False
			self._mnuGuiEditor.Enabled = True
			self.editormode = self.EDITOR_MODE_TEXT
		else:
			self._textBox1.Height = self.textBoxMinHeight
			self._textBox1.Width = self.textBoxMinWidth
			self._mnuEdit.Enabled = True
			self._panelGUI.Visible = True
			self._mnuTextEditor.Enabled = True
			self._mnuGuiEditor.Enabled = False
			self.editormode = self.EDITOR_MODE_GUI
			
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
				self._mnuView.Enabled = False
				self._mnuFile.Enabled = False	
				self._mnuEdit.Enabled = False				
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
#			self._buttonSave.Visible = False
#			self._mnuFile.Enabled = False
			self._saveToolStripMenuItem.Enabled = False
			self._saveAsToolStripMenuItem.Enabled = False
			self._restorelStripMenuItem1.Enabled = False
			self._mnuEdit.Enabled = False
			self._mnuView.Enabled = False
			self.editormode = self.EDITOR_MODE_TEXT
		else:
			self.loadGroups()
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
		self._buttonFind.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._buttonFind.Image = System.Drawing.Image.FromFile(globalvars.IMAGESEARCH)
		self._buttonGotoLine.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image
		self._buttonGotoLine.Image = System.Drawing.Image.FromFile(globalvars.IMAGESEARCH)
#		self._pictureBoxTrashValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
#		self._pictureBoxTrashCriteriaFirst.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._cmdLineToGui.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDOWN)
		self._cmdAddCriteria.Image = System.Drawing.Image.FromFile(globalvars.IMAGEADD)
		self._cmdTrashCriteria.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._cmdAddValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEADD)
		self._cmdTrashValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._cmdRemoveLine.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._copyCurrentLineToVisualEditorToolStripMenuItem.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDOWN)
		self._removeCurrentLineToolStripMenuItem.Image = System.Drawing.Image.FromFile(globalvars.IMAGEDELETE_SMALL)
		self._mnuTextEditor.Image = System.Drawing.Image.FromFile(globalvars.IMAGETEXT)
		self._mnuGuiEditor.Image = System.Drawing.Image.FromFile(globalvars.IMAGELIGHTNING)
#		self._buttonAddCriteria.Text = ''
#		self._buttonAddValues.Image = System.Drawing.Image.FromFile(globalvars.IMAGEADD)
#		self._buttonAddValues.Text = ''

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
		self.setComboModifiers()
		self.loadGroups()
		self._textBox1.SelectionStart = 0
		self._textBox1.SelectionStart = 1

		self.setEditorMode(self.editormode)
		
		self.setLineInfo()



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
		self.setComboModifiers()
#		myKey = self._comboCriteriaFields.SelectedValue
#		self._comboKeyModifiers.DataSource = sorted(rulefile.getAllowedKeyModifiers(myKey))


	def ComboValueFieldsSelectedIndexChanged(self, sender, e):
		self.setComboModifiers()
#		myKey = self._comboValueFields.SelectedValue
#		self._comboValueModifiers.DataSource = rulefile.getAllowedValModifiers(myKey)

	def setComboModifiers(self):
		myKey = self._comboCriteriaFields.SelectedValue
		self._comboKeyModifiers.DataSource = sorted(rulefile.getAllowedKeyModifiers(myKey))	
		myKey = self._comboValueFields.SelectedValue
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
		if self.clearValuesAfterAdding == True:
			self._textBoxCriteria.Text = ''
			self._textBoxValues.Text = ''
			self._textBoxCompleteCriteria.Text = ''
			self._textBoxCompleteValues.Text = ''
		return
			

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


		
	def CheckBoxClearValuesAfterAddingCheckedChanged(self, sender, e):
		self.clearValuesAfterAdding = self._checkBoxClearValuesAfterAdding.Checked

	def SaveToolStripMenuItemClick(self, sender, e):
		self.writeRuleFile()
		self.loadGroups()

	def ButtonCloseClick(self, sender, e):
		self.Close()
	
	def CloseToolStripMenuItemClick(self, sender, e):
		self.Close()

	def SaveAsToolStripMenuItemClick(self, sender, e):
		saveAsDialog = SaveFileDialog()
		saveAsDialog.Filter = 'Data Manager rule set (*.dat)|*.dat'
		if saveAsDialog.ShowDialog() == DialogResult.OK:
			self.writeRuleFile()
			self.loadGroups()
			try:
				File.Copy(globalvars.DATFILE,saveAsDialog.FileName)
			except Exception, err:
				MessageBox.Show('Could not save file.\n%s' % str(err), 'Data Manager for ComicRack %s' % globalvars.VERSION)
		return

	def RestorelStripMenuItem1Click(self, sender, e):
		openFileDialog = OpenFileDialog()
		openFileDialog.Filter = 'Data Manager rule set (*.dat)|*.dat'
		if openFileDialog.ShowDialog() == DialogResult.OK:
			self.writeRuleFile()
			self.loadGroups()
			try:
				File.Copy(globalvars.DATFILE,globalvars.BAKFILE,True)
				File.Copy(openFileDialog.FileName, globalvars.DATFILE, True)
				self.showTheFile()
			except Exception, err:
				MessageBox.Show('Could not restore file.\n%s' % str(err), 'Data Manager for ComicRack %s' % globalvars.VERSION)
			
		pass

	def AboutTheDataManagerToolStripMenuItemClick(self, sender, e):
		theForm = aboutForm()
		theForm.ShowDialog()
		theForm.Dispose()

	def TextBox1Leave(self, sender, e):
		if self._textBox1.SelectionLength == 0:
			self._textBox1.SelectionLength = 1
			
	def ButtonGotoLineClick(self, sender, e):
		self.selectLine(int(self._textBoxSelectLine.Text) - 1)
		self.setLineInfo()

	def CmdTrashCriteriaClick(self, sender, e):
		self._textBoxCompleteCriteria.Text = ''

	def CmdTrashValuesClick(self, sender, e):
		self._textBoxCompleteValues.Text = ''

	def CmdLineToGuiClick(self, sender, e):
		if self._textBoxCompleteCriteria.Text + self._textBoxCompleteValues.Text == '':
			self.copyLineToGui()
		else:
			if MessageBox.Show('Do you want to replace the current content in the visual editor?','Data Manager for ComicRack %s' % globalvars.VERSION,MessageBoxButtons.YesNo) <> System.Windows.Forms.DialogResult.No:
				self.copyLineToGui()
		return
	
	def copyLineToGui(self):
#		MessageBox.Show(str(self.currentLine()))
		myLine = self.lineContent(self.currentLine())
		tmp = myLine.split('=>')
		self._textBoxCompleteCriteria.Text = tmp[0].strip()
		self._textBoxCompleteValues.Text = tmp[1].strip()
	
	def removeLine(self,line, askConfirm = True):
		# removes line 'line' from buffer
		# note: lines start with index 0
		# if askConfirm is set to True it will ask for confirmation first
		self.selectLine(self.currentLine())
		if askConfirm == True:
			if MessageBox.Show('Are you sure you want to delete this line?\nYou cannot undo this.', 
				'Data Manger for ComicRack %s' % globalvars.VERSION, 
				MessageBoxButtons.YesNo) == DialogResult.No:
				return
		line = int(line)
		myBuffer = self._textBox1.Text.split(System.Environment.NewLine)
		if line > len(myBuffer) - 1: return False
		tmp = []
		i = 0
		for l in myBuffer:
			if i <> line: tmp.Add(l)
			i += 1
		newBuffer = System.Environment.NewLine.join(tmp)
		self._textBox1.Text = newBuffer	
		self.selectLine(line)	
		return True
		
	def currentLine(self):
		return self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
	
	def lineLength(self, line):
		# returns the length of line 'line'
		# returns 0 if line out of index
		# note: lines start with index 0
		line = int(line)
		tmp = self._textBox1.Text.split(System.Environment.NewLine)
		if line > len(tmp) - 1: return 0		
		return len(tmp[line])
	
	def lineContent(self,line):
		# returns the texxt of line 'line'
		# returns '' if line out of index
		# note: lines start with index 0
		line = int(line)
		tmp = self._textBox1.Text.split(System.Environment.NewLine)
		if line > len(tmp) - 1: return 0
		return tmp[line]
		
		
	def selectLine(self,line):
		'''
		highlights the line 'line'
		attention: lines start with index 0
		'''
		line = int(line) 
#		tmp = self._textBox1.Text.split(System.Environment.NewLine)

#		MessageBox.Show(tmp[line])
#		myLength = len(tmp[line])
		self._textBox1.SelectionStart = self._textBox1.GetFirstCharIndexFromLine(line)
		self._textBox1.SelectionLength = self.lineLength(line)
		self._textBox1.ScrollToCaret()


	def CmdRemoveLineClick(self, sender, e):
		self.removeLine(self.currentLine(), True)


	def MnuTextEditorClick(self, sender, e):
		self.setEditorMode(self.EDITOR_MODE_TEXT)

	def MnuGuiEditorClick(self, sender, e):
		self.setEditorMode(self.EDITOR_MODE_GUI)