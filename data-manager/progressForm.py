import System.Drawing
import System.Windows.Forms
import System.Threading

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
from globalvars import *

class progressForm(Form):
	def __init__(self, theText = ''):
		self.InitializeComponent()
		self.progValue = 0
		self.labelText = theText
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.Text = 'Data Manager for ComicRack %s' % globalvars.VERSION
	
	def InitializeComponent(self):
		self._progressBar = System.Windows.Forms.ProgressBar()
		self._label1 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# progressBar
		# 
		self._progressBar.Location = System.Drawing.Point(12, 39)
		self._progressBar.Name = "progressBar"
		self._progressBar.Size = System.Drawing.Size(413, 23)
		self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._progressBar.TabIndex = 0
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.BackColor = System.Drawing.SystemColors.Control
		self._label1.Location = System.Drawing.Point(13, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(22, 13)
		self._label1.TabIndex = 1
		self._label1.Text = "xxx"
		# 
		# progressForm
		# 
		self.ClientSize = System.Drawing.Size(436, 84)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._progressBar)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "progressForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "progressForm"
		self.Load += self.ProgressFormLoad
		self.ResumeLayout(False)
		self.PerformLayout()


	def ProgressFormLoad(self, sender, e):
		self._label1.Text = self.labelText
	