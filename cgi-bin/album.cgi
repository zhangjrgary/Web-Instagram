#!/usr/bin/env python

import os
import cgi
import cgitb
import subprocess
import sys

print "Content-Type: text/html\n\n"

print "<head><body>"

saveDir = '/var/www/html/newphoto/' # Full path or relative path
readDir = '/newphoto/'

filelist = os.listdir(saveDir)

#print filelist

def compareFt(fa,fb):
	if(os.path.getmtime(saveDir+fa) > os.path.getmtime(saveDir+fb))	:
		return -1
	else:
		return 1
def printGrid(num):
	#print num
	try:
		print '<td>' 
		print '<a href="%s">' % (readDir+filelist[num-1])
		print '<img src="%s" style="max-width:200px;max-height:200px;" >' % (readDir+filelist[num-1])
		print '</td>'
	except:
		print '<td>' 
		print ''
		print '</td>'
		
filelist.sort(compareFt)
form = cgi.FieldStorage()
print type(form)
try : page = int(form['page_num'].value)
except : page = 0
try : page = int(form['page_num1'].value) -1 
except : page = page
Num= int(page) * 8 + 1
#print page
max_page=len(filelist) / 8 
#print max_page
print '<table style="width:100%">'
print '<tr>'
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
print '</tr>'
print '<tr>'
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
printGrid(Num)
Num = Num + 1
print '</tr>'
print '</table>'

if page!=0:
	print '''<form action="album.cgi" method="POST">
	<input type="hidden" value="%d" name="page_num">
	<input type="submit" value="Page Up" name="page">
	</form>''' % (page-1)

#print "Now is in %d/%d" % (page+1,max_page+1)
if page!=max_page:
	print '''<form action="album.cgi" method="POST">
	<input type="hidden" value="%d" name="page_num">
	<input type="submit" value="Page Down" name="page">
	</form>''' % (page+1)

#print "jump to "
print '''<form action="album.cgi" method="POST">
<input type="number" value="%d" name="page_num1" min="1" max="%d"> /%d
</form> ''' % ((page+1),max_page+1,max_page+1)

print '<a href="../index.html">Index</a>'
#print '<a href="editor.cgi?fn=%s">Edit Photo</a>' % (filename)

print '</body></head>'