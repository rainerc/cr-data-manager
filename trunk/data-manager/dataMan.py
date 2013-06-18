'''
replaceData

plugin script for ComicRack to replace field content in the library
based on user-defined conditions
the rules are read from file replaceData.dat, located in the script directory

The CR Data Manager plugin is licensed under the Apache 2.0 software
license, available at: http://www.apache.org/licenses/LICENSE-2.0.html

v 1.0 RC1

by docdoom

GUI by T3KNOGHO57

images and icons used by permission of 600WPMPO and www.aha-soft.com

revision history:

r149 (RC1)
fixed - combination of numerical key and Null value like <<Count:>> raised Exception
bug - if a large set of books is selected then the second progressbar will freeze
fixed - if an Exception is thrown while executing the rules the for loop continues running
change - using the backgroundWorker to handle the main loops
fixed - erratic error: expecting an indented block (issue 66). Code now is written to memory, 
        not to file as before
change - includes GUI 0.1.0r8 RC9

r150 (RC2)
fixed - user.ini was overwritten by installation (issue 70, was missing in keepfiles parameter)
fixed - Exception in stringRemoveLeading (str.startsWith() used instead of str.startswith() )
change - includes GUI 0.1.1r10

r151 (1.0.1)
change - added string fields BookAge,BookCondition,BookLocation to dataman.ini (issue 68)
fixed - range modifiers GreaterEq etc. might give unexpected results (issue 71)
fixed - progress form now supports cancellation while running over the selected books

r152 (1.0.1)
change - included GUI 0.1.1r11

r154 (1.0.2)
change - GUI tab order corrected
change - GUI supports import / export of groups
change - GUI supports import option
change - GUI: Text edit of Rulesets (in the ruleset panel) now always visible
change - GUI: window is resizable
change - included GUI 0.1.1r18

r155 (1.0.3)
fixed - cancellation of backgroundworker did not work as expected (issue 74)
fixed - Data Manger won't run in a combined script after CV Scraper (issue 75)

r156 (1.0.4)
fixed - error when assigning a Null value to numerical fields (issue 76)
fixed - error message has meaningless line number (issue 77)
fixed - user cannot cancel parsing a *very* large ruleset collection (issue 78)

r162 (1.0.5)
change - added Manga, LanguageISO and all YesNo fields (issue 58)
change - added BookPrice, CommunityRating, Rating (issue 65)

r164 (1.0.5)
change - added GUI r21
fixed - GUI: click on row header throws error if cell edit not confirmed

r165 (1.0.6)
fixed - writing non-ascii characters to log output raises error (issue 80) 

r166 (1.0.7)
change - GUI: single Instance of gui only.
change - GUI: Changed handling of LanguageISOs (fixes issue 81)
added - GUI: Disable Confirmation of Default Profile Save (at the top of the Utilities Menu.)
added - GUI: startup debug log to track further startup problems.
change - GUI: updated handling of limited value items in Templates (YesNo, LanguageISOs, MangaYesNo).
change - GUI: made menus more user friendly, you no longer have to focus on the drop down arrow to activate menu, clicking the dropdown menu will activate it)
change - added GUI r25

r171 (1.1.0)
fixed - GUI: Custom value in rule was taking value from action instead of rule textbox
fixed - GUI: custom keys and modifiers now read from ini file.
fixed - GUI: Custom value adaptation for templates.
change - added custom fields (issue 60)
change - added dateTime fields - todo: CALC modifier for action part of dateTime?
change - added GUI r31

r174 (1.1.0)
fixed: <<Custom(xxx):>> does not return any books with empty Custom(xxx), had to be set to 'None'
fixed: yesandrighttoleft value left out for manga (issue 84)
fixed: multiValueAdd and multiValueRemove accept multiple values (issue 67)
change - Calc modifier supports DateTime fields
change - GUI: DateTime fields support
change - GUI: entries with calc modifier are validated within GUI
fixed - {Field} is now allowed in all actions (issue 82)
fixed - removeLeading returns None if leading string is not found
change - includes GUI r40

r 176 (1.1.0)
change - implemented parser.parseCalc() and user defined DateTime format  (issue 86)
change - parseCalc() supports Calc modifier
change - parseCalc() supports Add and MultiValueAdd

r177 (1.1.0)
change - parseCalc() supports dmString.replace and multiValue.replace
change - parseCalc() supports dmString.remove and multiValue.remove
change - parseCalc() supports dmString.removeLeading

r178 (1.1.0)
change - parseCalc() supports dmString.setValue
change - parseCalc() supports dmDateTime.setValue
change - parseCalc() supports dmNumeric.setValue

r179 (1.1.0)
change - parseCalc() supports dmYesNo.setValue

r 181 (1.1.0)
change - parseCalc() supports dmMangaYesNo.setValue

r182 (1.1.0)
change - actions are checked for syntax errors which are written to the logfile
change - includes GUI r47

r 183 (1.1.0)
fix - modifier Add raises error if no field variable {field} is used
change - includes GUI r48

r 186 (1.1.0)
change - the action which raised an error is written to the logfile
fixed - backgroundWorker can be cancelled only after the complete ruleset collection on a book is finished  (issue 88)
changed - minor performance improvements

r 188 (1.1.0)
change - BreakAfterFirstError in user.ini defines if DataMan should stop executing when an error is found
change - logfile results are written to memory first instead of file
change - references to ComicRack.Engine removed from comparer.init and dmString.init
change - includes GUI r49

r190 (1.1.0)
fixed - error when modifier Replace is used

r192 (1.2.0)
change - re-writing of parser started
change - new modifier NotContainsAllOf
change - basic re-writing of parser finished, tests still pending

r202 (1.2.0) - beta release
change - new modifier NotRange
change - tests of re-written parser finished
change - if a field is changed by one ruleset but multiple actions only the last value is written to the logfile
change - delimiter for multiple list items is changed from comma to '||'
change - includes GUI r53

r203 (1.2.0) - beta release
fixed - writing custom field value to log file throws exception (issue 93)

r204 (1.2.0) - non-release
change - basic OR rule mode implemented
change - rule mode is reflected in log file output

r205 (1.2.0) - beta release
fixed - DateTime not written in user defined format (issue 94)
fixed - error when a field containing a NewLine is touched by Calc (issue 95)
change - includes GUI r54

r206 (1.2.0 RC1)
change - includes GUI r55

r207 (1.2.0 RC2)
fixed - dmparser.equals returns case-sensitive comparison (not compatible to older DM versions) (issue 97)
fixed - old value of book.Tags is empty when written to the log (issue 98)
change - includes GUI r56

r208 (1.2.0 RC3)
change - includes GUI r58

r211 (1.2.0)
change - includes GUI r60

r212 (1.2.1)
fix - compare of Null value custom field does not work (issue 105)

r214 (1.2.2 beta)
change - new modifiers RegEx, NotRegEx, RegExReplace
change - includes GUI r62

r215 (1.2.2 beta) 
change - LogBookOnlyWhenValuesChanged key implemented (issue 100)

r216 (1.2.2 beta) 
fixed - quantifier expression between { and } in regex is mistaken for {field} reference (issue 108)

<< half-way through with replacing globalvars.VERSION with iniFile.read('Version') >>

todo - check valid modifiers in validate()
todo - read version info from dataman.ini
todo - cleanup configuratorForm (only needed from now on to display the log file)

>> revision history for older releases is at http://code.google.com/p/cr-replace-data/wiki/RevisionLog

ideas:
replace globalvars with entries from dataman.ini
todo: modifier Before
todo: modifier After
todo: use In as modifier in keys
     e.g. <<Number.In:1,3,8>>
todo: add RegExp as modifier
todo: simulation instead of actual replacing of data
------------------------------------------------------
'''

import clr
import sys
import re
import System
import System.Text
from System import String
from System.IO import File,  Directory, Path, FileInfo, FileStream
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *
import dmutils
from dmutils import iniFile, parser, dmString
import globalvars
from displayResultsForm import displayResultsForm
from aboutForm import aboutForm
#from progressForm import progressForm
from dmProgressForm import dmProgressForm
from startupForm import startupForm
from configuratorForm import configuratorForm

myParser = parser()
dmString = dmString()

# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

DEBUG__ = False


#sys.path.append(globalvars.FOLDER)

def debug (s):
	if DEBUG__ == True:
		try:
			print str(s)
		except Exception, err:
			print s
	return

def writeVersion():
	''' not sure if we need this '''
	myIni = dmutils.iniFile()
	myIni.write('Version',globalvars.VERSION)
	

def dmConfig():
	'''
	runs the ruleset collection editor depending on the value of key GUI in user.ini
	if GUI == anything other than the value 'Old' it will run the exe defined in
	globalvars, else if will run the old minimalistic gui
	type: void
	'''
	myIni = iniFile(globalvars.USERINI)
	myGui = myIni.read('Gui')
	version = myIni.read('Version')
	
	if myGui <> 'Old':
		import System.Diagnostics
		p = System.Diagnostics.Process()
		p.StartInfo.FileName = globalvars.GUIEXE
		p.Start()
	else:
		form = configuratorForm()
		form.setFile(globalvars.DATFILE)
		form.Text = 'Data Manager Configurator %s' % version
		form.ShowDialog(ComicRack.MainWindow)
		form.Dispose()

def crVersion():
	''' checks the CR version if it is min. 0.9.164 (for custom values) '''
	minVersion = '0.9.164'		# we need CR 0.9.164 minimum (for custom values)
	vMin = 0 + 9000 + 164
	myVersion = ComicRack.App.ProductVersion	# get the installed CR version number
	v = myVersion.split('.')
	vMyVersion = (int(v[0]) * 1000000) + (int(v[1]) * 1000) + int(v[2])
	if vMyVersion < vMin:		# if actual version is lower than minimum version: return False
		MessageBox.Show(
		'You have only CR version %s installed.\nPlease install at least version %s of ComicRack first!' % (myVersion,minVersion),
		'Data Manger for ComicRack %s' % globalvars.VERSION)
		return False
	return True

class dates:
	
	def __init__(self):
		pass
	
	def stringToDate(self,theString):
		theDate = Sytem.DateTime.Parse(theString)
		return theDate
	

# ============================================================================      
# hook to run the configScript
#@Name	 Data Manager configuration
#@Key    data-manager
#@Hook   ConfigScript
# ============================================================================      
def dataManagerConfig():
	dmConfig()


# ============================================================================ 
# hook to run the main dataManager loop
#@Name	Data Manager
#@Image dataMan16.png
#@Key	data-manager
#@Hook	Books
# ============================================================================     

def replaceData(books):

	ERROR_LEVEL = 0

	if not crVersion():	return		# ComicRack version ok?

	s = File.ReadAllLines(globalvars.DATFILE)
	if not s[0].startswith('#@ VERSION'):
		MessageBox.Show('Your configuration needs conversion.\nPlease use the configurator first.','Data Manager %s' % globalvars.VERSION)
		return

	ini = dmutils.iniFile(globalvars.USERINI)
	if ini.read('ShowStartupDialog') == 'False':
		pass
	else:
		theForm = startupForm()
		theForm.ShowDialog()
		theForm.Dispose()

		if theForm.DialogResult == DialogResult.Yes:		# closed with Yes button
			pass
		elif theForm.DialogResult == DialogResult.Cancel:	# closed with window close button
			return
		elif theForm.DialogResult == DialogResult.No:		# closed with No button
			return
		elif theForm.DialogResult == DialogResult.Retry:	# closed with configure button
			dmConfig()
			return
	
	try:		# delete temporary files from last data manager run
		File.Delete(globalvars.TMPFILE)
		File.Delete(globalvars.ERRFILE)
		File.Delete(globalvars.LOGFILE)
	except Exception, err:
		MessageBox.Show('One of the temporary files of the Data Manager could not be deleted.\nPlease restart ComicRack.')
		return
		

	# check if the default ruleset collection exists
	if not File.Exists(globalvars.DATFILE):
		MessageBox.Show('Please use the Data Manager Configurator first!','Data Manager %s' % globalvars.VERSION)
		return

	progBar = dmProgressForm(globalvars.PROCESS_BOOKS, books)		
	progBar.ShowDialog()

	if progBar.errorLevel == 0:
		msg = "Finished. I've inspected %d books.\nDo you want to take look at the log file?" % (progBar.stepsPerformed)
	
		form = displayResultsForm()
		form.configure(msg)
		form.ShowDialog(ComicRack.MainWindow)
		form.Dispose()

		if form.DialogResult == DialogResult.Yes:
	
			form = configuratorForm()
			form.setFile(globalvars.LOGFILE)
			form.Text = 'Data Manager Logfile %s' % globalvars.VERSION
			form.ShowDialog(ComicRack.MainWindow)
			form.Dispose()

	try:
		#File.Delete(TMPFILE)
		#File.Delete(globalvars.ERRFILE)
		pass
	except Exception, err:
		pass
	

