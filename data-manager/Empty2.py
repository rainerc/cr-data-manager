import System
from System.IO import Path, FileInfo
FOLDER = FileInfo(__file__).DirectoryName + "\\"

theDLL = Path.Combine(FOLDER, 'crdmcgui32.dll')
import clr
clr.AddReferenceToFileAndPath(theDLL)
import globalvars
from crdmcgui import gui


dmGUI = gui()
dmGUI.ShowDialog()