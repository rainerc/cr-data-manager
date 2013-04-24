import clr
import System
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *
from System.Drawing import *

import globalvars

class progressForm(Form):

	def __init__(self):
		self.Width = 360
		self.Height = 80
		self.StartPosition = FormStartPosition.CenterScreen
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Text = 'CR Data Manager Version %s' % globalvars.VERSION

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