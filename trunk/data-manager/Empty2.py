import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.IO import Path, FileInfo
import globalvars
	
def showStartup():
	from progressForm import progressForm
	theForm = progressForm('sdffdf')
	theForm.Show()


	pass


showStartup()