'''
new version of progressForm.py
'''

import System.Drawing
import System.Windows.Forms
import System.Threading
from System.IO import File

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
from globalvars import *

import dmutils
from dmutils import *

import dmparser
from dmparser import dmParser
dmParser = dmParser()

dmString = dmString()
userIni = iniFile(globalvars.USERINI)
userIni.write('LastScanErrors',0)
ERRCOUNT = 0

theLog = ""

# initialize this with
# 1.) for the run over the books:
# theForm = progressForm(PROCESS_BOOKS, books)
# 2.) for parsing the code:
# theForm = progressForm(PROCESS_CODE)


class dmProgressForm(Form):
	def __init__(self, theProcess = 0, books = None):
		self.InitializeComponent()
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.Text = 'Data Manager for ComicRack %s' % globalvars.VERSION
		self.theProcess = theProcess
		self.theBooks = books
		self.errorLevel = 0
		self.cancelledByUser = False
		self.stepsPerformed = 0
		self.maxVal = 0
		userIni = iniFile(globalvars.USERINI)
		self.dateTimeFormat = userIni.read('DateTimeFormat')
		self.stop_the_Worker = False	
		
		# this is a workaround for the error described in issue 98:
		# would love to use book.Clone() but here's the workaround:
		dmIni = iniFile(globalvars.INIFILE)
		self.allVals = dmIni.read('allowedVals').split(',')
		for field in self.allVals:
			setattr(self,'field_' + field, None)
	
	def InitializeComponent(self):
		self._progressBar = System.Windows.Forms.ProgressBar()
		self._label1 = System.Windows.Forms.Label()
		self._backgroundWorker1 = System.ComponentModel.BackgroundWorker()
		self._buttonCancel = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# progressBar
		# 
		self._progressBar.Location = System.Drawing.Point(12, 39)
		self._progressBar.Name = "progressBar"
		self._progressBar.Size = System.Drawing.Size(413, 23)
		self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._progressBar.TabIndex = 0
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.BackColor = System.Drawing.SystemColors.Control
		self._label1.Location = System.Drawing.Point(13, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(22, 13)
		self._label1.TabIndex = 1
		self._label1.Text = "xxx"
		# 
		# backgroundWorker1
		# 
		self._backgroundWorker1.WorkerReportsProgress = True
		self._backgroundWorker1.WorkerSupportsCancellation = True
		self._backgroundWorker1.DoWork += self.BackgroundWorker1DoWork
		self._backgroundWorker1.ProgressChanged += self.BackgroundWorker1ProgressChanged
		self._backgroundWorker1.RunWorkerCompleted += self.BackgroundWorker1RunWorkerCompleted
		#self._backgroundWorker1.CancellationPending += self.BackgroundWorker1Cancellation
		# 
		# buttonCancel
		# 
		self._buttonCancel.Location = System.Drawing.Point(185, 71)
		self._buttonCancel.Name = "buttonCancel"
		self._buttonCancel.Size = System.Drawing.Size(75, 23)
		self._buttonCancel.TabIndex = 2
		self._buttonCancel.Text = "Cancel"
		self._buttonCancel.UseVisualStyleBackColor = True
		self._buttonCancel.Click += self.ButtonCancelClick
		# 
		# progressForm
		# 
		self.ClientSize = System.Drawing.Size(436, 106)
		self.Controls.Add(self._buttonCancel)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._progressBar)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "progressForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "progressForm"
		self.FormClosing += self.ProgressFormFormClosing
		self.FormClosed += self.ProgressFormFormClosed
		self.Load += self.ProgressFormLoad
		self.Shown += self.ProgressFormShown
		self.ResumeLayout(False)
		self.PerformLayout()


	def ProgressFormLoad(self, sender, e):
		pass

	def BackgroundWorker1DoWork(self, sender, e):

		theLog = ''
		parserErrors = 0

		if self.theProcess == 0:		# just for testing
			i = 0
			while i <= 100:
				i += 1
				# Report progress to 'UI' thread
				self._backgroundWorker1.ReportProgress(i)
				# Simulate long task
				System.Threading.Thread.Sleep(100)
			return

		# ------------------------------------------------------
		# run the parsed code over the books:
		# ------------------------------------------------------
		


		userIni = iniFile(globalvars.USERINI)
		dtStarted = System.DateTime.Now

		if self.theProcess == globalvars.PROCESS_BOOKS:
			self.maxVal = self.theBooks.Length
			self._progressBar.Maximum = self.maxVal
			self._progressBar.Step = 1
			f=open(globalvars.LOGFILE, "w")	# open logfile

			s = File.ReadAllLines(globalvars.DATFILE)

			if not s[0].startswith('#@ VERSION'):
				MessageBox.Show('The configuration needs to be converted. Please start the configurator first.')
				return
			
			lines = []


			for line in s:
				if line == '#@ END_RULES': break
				if (not line.startswith('#')) and line.strip() <> '': lines.append(line)

			for book in self.theBooks:
				if not self._backgroundWorker1.CancellationPending: 
					self.stepsPerformed += 1
					self._backgroundWorker1.ReportProgress(self.stepsPerformed / self.maxVal * 100)
					
					# we use this for custom fields only because some other fields
					# might not be stored by book.Clone():
					theOriginalBook = book.Clone()	# to retrieve the original values later
					# for the remaining we use:
					for field in self.allVals:
						if field <> 'Custom': setattr(self,'field_' + field, getattr(book,field))
						
					for line in lines:
						if self.stop_the_Worker == True: break
						try:

							if dmParser.matchAllRules(line,book):
								joinChar = ' ' + dmParser.ruleMode + ' '
								theLog += '%s (%s) #%s was touched\t[%s]\n' % (unicode(book.Series),book.Volume,unicode(book.Number),joinChar.join(dmParser.rules))
								dmParser.executeAllActions(book)
								theLog += dmParser.theLog
								parserErrors += dmParser.errCount
								for fieldTouched in dmParser.fieldsTouched:
									# is: Custom(orig filename)
									if fieldTouched.startswith('Custom'):
										cField = fieldTouched.replace('Custom(','').strip(')')
										beforeTouch = theOriginalBook.GetCustomValue(cField)
										afterTouch = book.GetCustomValue(cField)
									else:
										#beforeTouch = getattr(theOriginalBook,fieldTouched)
										beforeTouch = getattr(self,'field_' + fieldTouched)
										afterTouch = getattr(book,fieldTouched)
									if afterTouch <> beforeTouch:
										theLog += '\t%s old: %s\n' % (fieldTouched, unicode(beforeTouch))
										theLog += '\t%s new: %s\n' % (fieldTouched, unicode(afterTouch))
								if parserErrors > 0 and userIni.read("BreakAfterFirstError") == 'True':
									self.stop_the_Worker = True
									break
						except Exception, err:
							print str(Exception.args)
							MessageBox.Show('An unhandled error occurred while executing the rules. \n%s\nPlease check your rule: %s' % (str(err),line), 'Data Manager - Version %s' % globalvars.VERSION)
							self.errorLevel = 1
							self.stop_the_Worker = True
							break

				else:
					theLog += ('\n\nExcecution cancelled by user.')
					self.cancelledByUser = True
					break
				if self.stop_the_Worker == True: break
				
			dtEnded = System.DateTime.Now
			dtDuration = dtEnded - dtStarted
			userIni.write('ParserStarted',str(dtStarted))
			userIni.write('ParserEnded',str(dtEnded))
			userIni.write('ParserDuration',str(dtDuration))

			if parserErrors > 0:
				MessageBox.Show('There were errors in your rules. You really should check the logfile!')

			f.write(theLog)
			f.close()
		return
			

	def BackgroundWorker1ProgressChanged(self, sender, e):
		# progressBar.Value = xxx  did not update the progressBar properly
		# so we use PerformStep()
		self._progressBar.PerformStep()
		if self.theProcess == globalvars.PROCESS_BOOKS:
			self._label1.Text = 'Data Manager worked on %d books' % self.stepsPerformed
		elif self.theProcess == globalvars.PROCESS_CODE:
			self._label1.Text = 'Data Manager parsed %d rules' % self.stepsPerformed
		return

	def BackgroundWorker1RunWorkerCompleted(self, sender, e):
		self.Close()
		pass

	def ProgressFormShown(self, sender, e):
		self._backgroundWorker1.RunWorkerAsync()
		
	def ButtonCancelClick(self, sender, e):
		self._backgroundWorker1.CancelAsync()
		pass
	
	def ProgressFormFormClosed(self, sender, e):
		self._backgroundWorker1.CancelAsync()

		
	def ProgressFormFormClosing(self, sender, e):
		self._backgroundWorker1.CancelAsync()

	def BackgroundWorker1Cancellation(self, sender, e):
		self.stop_the_Worker = True


