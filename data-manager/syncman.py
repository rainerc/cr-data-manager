# criteria for duplicates (books to be synchronized)
# Series
# Volume
# Number
# Year
# Month
# Format

# content to be synchronized
# read (mark as read, unread)
# rating

#@PCount 1
#@Enabled True

# playing around with datetime


import datetime
from datetime import date

def testDateTime():

	dt = datetime.date(2013,1,12)
	myCurrentDate = date.today()
	
	print dt > myCurrentDate
	
class myDateTime(object):
	
	def stringToDate(self, s):
		tmp = s.split('/')
		return datetime(tmp[0],tmp[1],tmp[2]
	
	


#@Name     [Code Sample] All Books starting with
#@Hook     CreateBookList
#@Description Sample script to show how to write custom smartlist scripts

def GetBooksWith (books, a, b):

   newList = []    

   for book in books:

       if book.ShadowSeries.startswith(a):

           newList.append(book)

   return newList

# ============================================================================ 
# hook to run the main dataManager loop
#@Name	Data Synchronizer
#@Image dataMan16.png
#@Key	data-sync
#@Hook	Books
# ============================================================================     

def doSync(books):
	for book in books:
		print book.ReadPercentage
		

		
#		book.ReadPercentageAsRead = 20.3

		
		print 'asRead: %s' % str(book.ReadPercentageAsRead)
		print book.ReadPercentageAsText
		book.MarkAsRead()
		print book.ReadPercentage
		
#		print dir(book)
		print book.AddedTime
		
		book.LastPageRead = 5	# only chance to set the readpercentag

		myReadPercentage = book.LastPageRead * 100 / book.PageCount
		print 'lastpage: %d' % book.LastPageRead
		print 'pagecount: %d' % book.PageCount
		print 'percentage: %d.2' % float(myReadPercentage)
		
#		print dir(book.CopyDataFrom)
		
	myBooks = ComicRack.App.GetLibraryBooks()
#	print dir(myBooks)
	for book in myBooks:
		pass
	print "end"