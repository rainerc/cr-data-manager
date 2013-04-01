
import clr
import System
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *
from System.Drawing import *

import globalvars

class aboutForm(Form):
	
	def __init__(self):
		self.Width = 380
		self.Height = 250
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = True
		self.Text = 'CR Data Manager %s' % globalvars.VERSION

		self.label = Label()
		self.label.Location = Point(90, 20)
		self.label.Width = 280
		self.label.Height = 110
		self.label.Text = ('The CR Data Manager plugin is licensed under the Apache 2.0 software ' +
			'license, available at:\nhttp://www.apache.org/licenses/LICENSE-2.0.html\n\n' +
			'Big thanks go to 600WPMPO and Casublett: without ' + 
			'their help the plugin would not work as it does now.\n\nImportant links:')

		self.linklabelManual = LinkLabel()
		self.linklabelManual.Location = Point(90,135)
		self.linklabelManual.Text = 'Manual'
		self.linklabelManual.LinkClicked += self.manual

		self.linklabelWiki = LinkLabel()
		self.linklabelWiki.Location = Point(90,155)
		self.linklabelWiki.Text = 'Wiki'
		self.linklabelWiki.LinkClicked += self.wiki

		self.linklabelDonation = LinkLabel()
		self.linklabelDonation.Location = Point(90,175)
		self.linklabelDonation.Text = 'Donations'
		self.linklabelDonation.LinkClicked += self.donate	
			
		self.picturebox = PictureBox()
		self.picturebox.Location = Point(10,10)
		self.picturebox.Image = System.Drawing.Image.FromFile(globalvars.IMAGE)
		self.picturebox.Height = 70
		self.picturebox.Width = 70
		self.picturebox.SizeMode = PictureBoxSizeMode.StretchImage
		
		self.buttonClose = Button()
		self.buttonClose.Location = Point(290,200)
		self.buttonClose.Text = 'Close'
		self.buttonClose.DialogResult = DialogResult.Cancel
		self.Controls.Add(self.picturebox)
		self.Controls.Add(self.buttonClose)
		self.Controls.Add(self.label)
		self.Controls.Add(self.linklabelDonation)
		self.Controls.Add(self.linklabelManual)
		self.Controls.Add(self.linklabelWiki)

	def donate(self, sender, event):
		System.Diagnostics.Process.Start(DONATE)

	def manual(self, sender, event):
		System.Diagnostics.Process.Start(MANUAL)

	def wiki(self, sender, event):
		System.Diagnostics.Process.Start(WIKI)
		pass