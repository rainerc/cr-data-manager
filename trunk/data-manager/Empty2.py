import clr
import System
from System.IO import Path, FileInfo
import globalvars
FOLDER = FileInfo(__file__).DirectoryName + "\\"

theDLL = Path.Combine(FOLDER, 'crdmcgui-0.9r23.dll')

#clr.AddReferenceToFileAndPath(theDLL)
clr.AddReference('crdmcgui-0.9r23.dll')

from crdmcgui import gui


dmGUI = gui()
dmGUI.ShowDialog()