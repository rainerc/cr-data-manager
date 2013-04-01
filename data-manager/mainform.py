import clr
import System
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *
from System.Drawing import *

import globalvars

class mainForm(Form):

	def __init__(self):
		self.Width = 285
		self.Height = 150
		self.MaximizeBox = False
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = True
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.Text = 'CR Data Manager %s' % globalvars.VERSION
		
		self.label = Label()
		self.label.Location = Point(90,20)
		self.label.Text = 'Welcome to the Data Manager.\n\nClick on the icon for more information.'
		self.label.Width = 300
		self.label.Height = 50

		self.picturebox = PictureBox()
		self.picturebox.Location = Point(10,10)
		self.picturebox.Image = System.Drawing.Image.FromFile(globalvars.IMAGE)
		self.picturebox.Height = 70
		self.picturebox.Width = 70
		self.picturebox.SizeMode = PictureBoxSizeMode.StretchImage
		self.picturebox.Cursor = Cursors.Hand
		self.picturebox.Click += self.aboutDialog
		
		self.tooltip1 = ToolTip()
		self.tooltip1.AutoPopDelay = 5000
		self.tooltip1.InitialDelay = 1000
		self.tooltip1.ShowAlways = True 
		self.tooltip1.SetToolTip(self.picturebox, "click on the image for more information")
		
		self.buttonRun = Button()
		self.buttonRun.Location = Point(10,90)
		self.buttonRun.Width = 120
		self.buttonRun.Text = 'Run the DataMan'
		self.buttonRun.DialogResult = DialogResult.OK

		self.buttonConfig = Button()
		self.buttonConfig.Location = Point(150,90)
		self.buttonConfig.Width = 120
		self.buttonConfig.Text = 'Configure'
		self.buttonConfig.DialogResult = DialogResult.No

		self.Controls.Add(self.label)
		self.Controls.Add(self.buttonRun)
		self.Controls.Add(self.buttonConfig)
		self.Controls.Add(self.picturebox)
		
	def aboutDialog(self, sender, event):
		form = aboutForm()
		form.ShowDialog(ComicRack.MainWindow)
		form.Dispose()