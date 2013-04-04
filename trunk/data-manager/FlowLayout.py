import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import Application
import FlowLayoutForm

Application.EnableVisualStyles()
form = FlowLayoutForm.FlowLayoutForm()
Application.Run(form)
