import clr
import System
clr.AddReference('System.Windows.Forms')
from System.IO import Path, FileInfo
import globalvars

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
	
theDllCall()