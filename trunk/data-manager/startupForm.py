
import System.Drawing
import System.Windows.Forms
import globalvars

from System.Drawing import *
from System.Windows.Forms import *

import dmutils
from dmutils import iniFile

class startupForm(Form):
	def __init__(self):
		self.InitializeComponent()
		self._pictureBox1.Image = System.Drawing.Image.FromFile(globalvars.IMAGE)
		iniFile = dmutils.iniFile()
		self.theVersion = iniFile.read('Version')
		self.Text = 'Data Manager for ComicRack %s' % self.theVersion
		self.Icon = Icon(globalvars.ICON_SMALL)
	
	def InitializeComponent(self):
		self._pictureBox1 = System.Windows.Forms.PictureBox()
		self._label1 = System.Windows.Forms.Label()
		self._buttonYes = System.Windows.Forms.Button()
		self._buttonNo = System.Windows.Forms.Button()
		self._buttonConfigure = System.Windows.Forms.Button()
		self._checkBox1 = System.Windows.Forms.CheckBox()
		self._pictureBox1.BeginInit()
		self.SuspendLayout()
		# 
		# pictureBox1
		# 
		self._pictureBox1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None
		self._pictureBox1.Location = System.Drawing.Point(13, 13)
		self._pictureBox1.Name = "pictureBox1"
		self._pictureBox1.Size = System.Drawing.Size(78, 78)
		self._pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._pictureBox1.TabIndex = 0
		self._pictureBox1.TabStop = False
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(109, 23)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(263, 78)
		self._label1.TabIndex = 1
		self._label1.Text = """This will run the Data Manager over the selected
books.

Do you want to start?"""
		# 
		# buttonYes
		# 
		self._buttonYes.DialogResult = System.Windows.Forms.DialogResult.Yes
		self._buttonYes.Location = System.Drawing.Point(13, 114)
		self._buttonYes.Name = "buttonYes"
		self._buttonYes.Size = System.Drawing.Size(116, 23)
		self._buttonYes.TabIndex = 2
		self._buttonYes.Text = "Yes"
		self._buttonYes.UseVisualStyleBackColor = True
		self._buttonYes.Click += self.Button1Click
		# 
		# buttonNo
		# 
		self._buttonNo.DialogResult = System.Windows.Forms.DialogResult.No
		self._buttonNo.Location = System.Drawing.Point(134, 114)
		self._buttonNo.Name = "buttonNo"
		self._buttonNo.Size = System.Drawing.Size(116, 23)
		self._buttonNo.TabIndex = 3
		self._buttonNo.Text = "No"
		self._buttonNo.UseVisualStyleBackColor = True
		# 
		# buttonConfigure
		# 
		self._buttonConfigure.DialogResult = System.Windows.Forms.DialogResult.Retry
		self._buttonConfigure.Location = System.Drawing.Point(256, 114)
		self._buttonConfigure.Name = "buttonConfigure"
		self._buttonConfigure.Size = System.Drawing.Size(116, 23)
		self._buttonConfigure.TabIndex = 4
		self._buttonConfigure.Text = "configure ..."
		self._buttonConfigure.UseVisualStyleBackColor = True
		# 
		# checkBox1
		# 
		self._checkBox1.Location = System.Drawing.Point(13, 143)
		self._checkBox1.Name = "checkBox1"
		self._checkBox1.Size = System.Drawing.Size(147, 24)
		self._checkBox1.TabIndex = 5
		self._checkBox1.Text = "Do not ask me again"
		self._checkBox1.UseVisualStyleBackColor = True
		self._checkBox1.CheckedChanged += self.CheckBox1CheckedChanged
		# 
		# startupForm
		# 
		self.AcceptButton = self._buttonYes
		self.CancelButton = self._buttonNo
		self.ClientSize = System.Drawing.Size(385, 168)
		self.Controls.Add(self._checkBox1)
		self.Controls.Add(self._buttonConfigure)
		self.Controls.Add(self._buttonNo)
		self.Controls.Add(self._buttonYes)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._pictureBox1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "startupForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "startupForm"
		self.FormClosed += self.StartupFormFormClosed
		self._pictureBox1.EndInit()
		self.ResumeLayout(False)


	def Button1Click(self, sender, e):
		pass

	def CheckBox1CheckedChanged(self, sender, e):
		pass

	def StartupFormFormClosed(self, sender, e):
		if self.DialogResult <> DialogResult.Cancel:
			ini = dmutils.iniFile(globalvars.USERINI)
			ini.write('ShowStartupDialog', str(not self._checkBox1.Checked))