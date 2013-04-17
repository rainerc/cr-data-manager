import clr
import sys
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import Application

import System.Text
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

import configuratorForm

import globalvars

Application.EnableVisualStyles()
form = configuratorForm.configuratorForm()
#Application.Run(form)
form.setFile(globalvars.DATFILE)
form.ShowDialog()
#form.Dispose()