
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import globalvars

class aboutForm(Form):
	def __init__(self):
		self.InitializeComponent()
		self._pictureBox1.Image = System.Drawing.Image.FromFile(globalvars.IMAGE)
		self.Text = 'Data Manager for ComicRack %s' % globalvars.VERSION
		self.Icon = Icon(globalvars.ICON_SMALL)
	
	def InitializeComponent(self):
		self._pictureBox1 = System.Windows.Forms.PictureBox()
		self._label1 = System.Windows.Forms.Label()
		self._linkLabel1 = System.Windows.Forms.LinkLabel()
		self._linkLabel2 = System.Windows.Forms.LinkLabel()
		self._linkLabel3 = System.Windows.Forms.LinkLabel()
		self._button1 = System.Windows.Forms.Button()
		self._pictureBox1.BeginInit()
		self.SuspendLayout()
		# 
		# pictureBox1
		# 
		self._pictureBox1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None
		self._pictureBox1.Location = System.Drawing.Point(12, 12)
		self._pictureBox1.Name = "pictureBox1"
		self._pictureBox1.Size = System.Drawing.Size(78, 78)
		self._pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._pictureBox1.TabIndex = 1
		self._pictureBox1.TabStop = False
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(107, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(309, 156)
		self._label1.TabIndex = 2
		self._label1.Text = "xx"
		# 
		# linkLabel1
		# 
		self._linkLabel1.Location = System.Drawing.Point(107, 173)
		self._linkLabel1.Name = "linkLabel1"
		self._linkLabel1.Size = System.Drawing.Size(129, 19)
		self._linkLabel1.TabIndex = 3
		self._linkLabel1.TabStop = True
		self._linkLabel1.Text = "Manual"
		self._linkLabel1.LinkClicked += self.LinkLabel1LinkClicked
		# 
		# linkLabel2
		# 
		self._linkLabel2.Location = System.Drawing.Point(107, 192)
		self._linkLabel2.Name = "linkLabel2"
		self._linkLabel2.Size = System.Drawing.Size(129, 19)
		self._linkLabel2.TabIndex = 4
		self._linkLabel2.TabStop = True
		self._linkLabel2.Text = "Wiki"
		self._linkLabel2.LinkClicked += self.LinkLabel2LinkClicked
		# 
		# linkLabel3
		# 
		self._linkLabel3.Location = System.Drawing.Point(107, 211)
		self._linkLabel3.Name = "linkLabel3"
		self._linkLabel3.Size = System.Drawing.Size(129, 19)
		self._linkLabel3.TabIndex = 5
		self._linkLabel3.TabStop = True
		self._linkLabel3.Text = "Donations"
		self._linkLabel3.LinkClicked += self.LinkLabel3LinkClicked
		# 
		# button1
		# 
		self._button1.DialogResult = System.Windows.Forms.DialogResult.OK
		self._button1.Location = System.Drawing.Point(341, 240)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(75, 23)
		self._button1.TabIndex = 6
		self._button1.Text = "Close"
		self._button1.UseVisualStyleBackColor = True
		# 
		# aboutForm
		# 
		self.ClientSize = System.Drawing.Size(428, 275)
		self.Controls.Add(self._button1)
		self.Controls.Add(self._linkLabel3)
		self.Controls.Add(self._linkLabel2)
		self.Controls.Add(self._linkLabel1)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._pictureBox1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "aboutForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "aboutForm"
		self.Load += self.AboutFormLoad
		self._pictureBox1.EndInit()
		self.ResumeLayout(False)


	def LinkLabel1LinkClicked(self, sender, e):
		System.Diagnostics.Process.Start(globalvars.MANUAL)

	def LinkLabel2LinkClicked(self, sender, e):
		System.Diagnostics.Process.Start(globalvars.WIKI)

	def LinkLabel3LinkClicked(self, sender, e):
		System.Diagnostics.Process.Start(globalvars.DONATE)

	def AboutFormLoad(self, sender, e):
		self._label1.Text = """The CR Data Manager plugin is licensed under the Apache 2.0 software 
			license, available at:\nhttp://www.apache.org/licenses/LICENSE-2.0.html
			
			idea and main program by docdoom
			rule editor GUI by KT3NOGHO57
						
			Big thanks go to 600WPMPO and Casublett: without
			their help the plugin would not work as it does now.\n\nImportant links:"""