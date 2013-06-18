# some variables for global use

import System
from System.IO import Path, FileInfo



FOLDER = FileInfo(__file__).DirectoryName + "\\"
DATFILE = Path.Combine(FOLDER, 'dataMan.dat')
SAMPLEFILE = Path.Combine(FOLDER, 'dataManSample.dat')
INIFILE = Path.Combine(FOLDER, 'dataMan.ini')
USERINI = Path.Combine(FOLDER, 'user.ini')
BAKFILE = Path.Combine(FOLDER, 'dataMan.bak')
ERRFILE = Path.Combine(FOLDER, 'dataMan.err')
TMPFILE = Path.Combine(FOLDER, 'dataMan.tmp')
LOGFILE = Path.Combine(FOLDER, 'dataMan.log')
CHKFILE = Path.Combine(FOLDER, 'dataMan.chk')		# will be created once the configuration is saved
GUIEXE = Path.Combine(FOLDER, 'crdmcgui.exe')

ICON_SMALL = Path.Combine(FOLDER, 'dataMan16.ico')
ICON = Path.Combine(FOLDER, 'dataMan.ico')
IMAGE = Path.Combine(FOLDER, 'dataMan.png')
IMAGESEARCH = Path.Combine(FOLDER, 'search.png')
IMAGEADD = Path.Combine(FOLDER, 'yes.png')
IMAGEAPPLY = Path.Combine(FOLDER, 'Apply.png')
IMAGETRASH = Path.Combine(FOLDER, 'Trash.png')
IMAGEDELETE_SMALL = Path.Combine(FOLDER, 'erase.png')
IMAGEDOWN = Path.Combine(FOLDER, 'down.png')
IMAGELIGHTNING = Path.Combine(FOLDER, 'lightning.png')
IMAGETEXT = Path.Combine(FOLDER, 'text.png')
DONATE = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UQ7JZY366R85S'
WIKI = 'http://code.google.com/p/cr-data-manager/'
MANUAL = 'http://code.google.com/p/cr-data-manager/downloads/list'

# the processes the backgroundWorker shall handle
PROCESS_CODE = 1
PROCESS_BOOKS = 2

#THECODE = []	# this will later on contain the parsed code


COMPARE_CASE_INSENSITIVE = True

#import dmutils
#from dmutils import iniFile
#print dir(dmutils)


#VERSION = ini.read('Version')
VERSION = '1.2.1 r216 beta'