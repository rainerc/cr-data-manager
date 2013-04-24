import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.IO import Path, FileInfo
import globalvars
from startupForm import startupForm

def testIni():
	import utils
	from utils import *
	
	myIni = utils.iniFile(globalvars.INIFILE)

	myIni.write('key1','val1')


def theDllCall():
	FOLDER = FileInfo(__file__).DirectoryName + "\\"
	
	theDLL = Path.Combine(FOLDER, 'crdmcgui.dll')
	
	#clr.AddReferenceToFileAndPath(theDLL)
	clr.AddReference('crdmcgui.dll')
	
	from crdmcgui import gui
	
	
	dmGUI = gui()
	dmGUI.ShowDialog()
	
def showStartup():
	from displayResultsForm import displayResultsForm
	from progressForm import progressForm
	from configuratorForm import configuratorForm
	from aboutForm import aboutForm
	theForm = aboutForm()
	theForm.ShowDialog()
	pass
	
showStartup()