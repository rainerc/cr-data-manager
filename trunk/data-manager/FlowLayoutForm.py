import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

i = 0

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
	'Genre',
	'Tags'
	]

numericalKeys = [
	'Volume',
	'Month',
	'Year',
	'Count'
	]

multiValueKeys = [
	'Tags',
	'Genre'
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
	'Genre',
	'Tags'
	]

allowedOperators = [
	'is (equal)',
	'contains',
	'starts with',
	'contains any of'
]

class FlowLayoutForm(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._flowLayoutPanel1 = System.Windows.Forms.FlowLayoutPanel()
		self._button2 = System.Windows.Forms.Button()
		self._comboBox1 = System.Windows.Forms.ComboBox()
		self._comboBox2 = System.Windows.Forms.ComboBox()
		self._textBox1 = System.Windows.Forms.TextBox()
		self._label1 = System.Windows.Forms.Label()
		self._checkBox1 = System.Windows.Forms.CheckBox()
		self._label2 = System.Windows.Forms.Label()
		self._label3 = System.Windows.Forms.Label()
		self._label4 = System.Windows.Forms.Label()
		self._flowLayoutPanel1.SuspendLayout()
		self.SuspendLayout()
		# 
		# flowLayoutPanel1
		# 
		self._flowLayoutPanel1.AutoScroll = True
		self._flowLayoutPanel1.Controls.Add(self._comboBox1)
		self._flowLayoutPanel1.Controls.Add(self._checkBox1)
		self._flowLayoutPanel1.Controls.Add(self._comboBox2)
		self._flowLayoutPanel1.Controls.Add(self._textBox1)
		self._flowLayoutPanel1.Location = System.Drawing.Point(12, 35)
		self._flowLayoutPanel1.Name = "flowLayoutPanel1"
		self._flowLayoutPanel1.Size = System.Drawing.Size(505, 274)
		self._flowLayoutPanel1.TabIndex = 1
		# 
		# button2
		# 
		self._button2.Location = System.Drawing.Point(15, 366)
		self._button2.Name = "button2"
		self._button2.Size = System.Drawing.Size(75, 23)
		self._button2.TabIndex = 2
		self._button2.Text = "button2"
		self._button2.UseVisualStyleBackColor = True
		self._button2.Click += self.Button2Click
		# 
		# comboBox1
		# 
		self._comboBox1.FormattingEnabled = True
		self._comboBox1.Location = System.Drawing.Point(3, 3)
		self._comboBox1.Name = "comboBox1"
		self._comboBox1.Size = System.Drawing.Size(121, 21)
		self._comboBox1.Sorted = True
		self._comboBox1.TabIndex = 0
		# 
		# comboBox2
		# 
		self._comboBox2.FormattingEnabled = True
		self._comboBox2.Location = System.Drawing.Point(176, 3)
		self._comboBox2.Name = "comboBox2"
		self._comboBox2.Size = System.Drawing.Size(121, 21)
		self._comboBox2.TabIndex = 1
		# 
		# textBox1
		# 
		self._textBox1.Location = System.Drawing.Point(303, 3)
		self._textBox1.Name = "textBox1"
		self._textBox1.Size = System.Drawing.Size(183, 20)
		self._textBox1.TabIndex = 2
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(139, 16)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(43, 19)
		self._label1.TabIndex = 3
		self._label1.Text = "Negate"
		# 
		# checkBox1
		# 
		self._checkBox1.Location = System.Drawing.Point(130, 3)
		self._checkBox1.Name = "checkBox1"
		self._checkBox1.Size = System.Drawing.Size(40, 24)
		self._checkBox1.TabIndex = 3
		self._checkBox1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		self._checkBox1.UseVisualStyleBackColor = True
		self._checkBox1.CheckedChanged += self.CheckBox1CheckedChanged
		# 
		# label2
		# 
		self._label2.Location = System.Drawing.Point(15, 16)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(100, 19)
		self._label2.TabIndex = 4
		self._label2.Text = "Field"
		# 
		# label3
		# 
		self._label3.Location = System.Drawing.Point(188, 16)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(100, 19)
		self._label3.TabIndex = 5
		self._label3.Text = "Range Modifier"
		# 
		# label4
		# 
		self._label4.Location = System.Drawing.Point(315, 16)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(100, 19)
		self._label4.TabIndex = 6
		self._label4.Text = "Value"
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(908, 463)
		self.Controls.Add(self._label4)
		self.Controls.Add(self._label3)
		self.Controls.Add(self._label2)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._button2)
		self.Controls.Add(self._flowLayoutPanel1)
		self.Name = "MainForm"
		self.Text = "wincontrols"
		self.Load += self.MainFormLoad
		self._flowLayoutPanel1.ResumeLayout(False)
		self._flowLayoutPanel1.PerformLayout()
		self.ResumeLayout(False)


	def Button2Click(self, sender, e):
		global i
		i += 1
		self.myButton = Button()
		
		self.myCombo = ComboBox()
		self.myCombo.Name = 'myKey%s' % str(i)
		self.myCombo.Items.AddRange(System.Array[System.Object](
			allowedKeys))
		self.myCombo.Sorted = True
		self._flowLayoutPanel1.Controls.Add(self.myCombo)
		
		self.myCheckBox = CheckBox()
		self.myCheckBox.Name = 'myNegator%s' % str(i)
		self._flowLayoutPanel1.Controls.Add(self.myCheckBox)
		
		i += 1
		self.myCombo = ComboBox()
		self.myCombo.Name = 'myOperator%s' % str(i)
		self.myCombo.Items.AddRange(System.Array[System.Object](
			allowedOperators))
		self._flowLayoutPanel1.Controls.Add(self.myCombo)
		
		i += 1
		self.myTextBox = TextBox()
		self.myTextBox.Name = 'myVal%s' % str(i)
		self.myTextBox.Size = System.Drawing.Size(183, 20)
		self._flowLayoutPanel1.Controls.Add(self.myTextBox)		
		
#		self.myButton.Name = 'myButton%s' % str(i)
#		self.myButton.Click += self.customClick
#		MessageBox.Show(self.myButton.Name)
#		self._flowLayoutPanel1.Controls.Add(self.myButton)
		pass
	
	def customClick(self, sender, e):
		MessageBox.Show('This is %s' % str(sender.Name))

	def MainFormLoad(self, sender, e):
		self._comboBox1.Items.AddRange(System.Array[System.Object](
			allowedKeys))
		self._comboBox2.Items.AddRange(System.Array[System.Object](
			allowedOperators))
		

	def CheckBox1CheckedChanged(self, sender, e):
		pass