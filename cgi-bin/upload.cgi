#!/usr/bin/env python

import os
import cgi
import cgitb
import subprocess
import sys

print "Content-Type: text/html\n\n"
print

cgitb.enable()

form = cgi.FieldStorage()

print '<html><body>'

saveDir = '/var/www/html/myupload' # Full path or relative path
readDir = '/myupload'

if not os.path.exists(saveDir):
    os.makedirs(saveDir)

if ('pic' not in form):
    print "No file uploaded: No photo be setected."
elif (not form['pic'].filename):
    print "No file selected. "
else:
    fileitem = form['pic']
    filename = fileitem.filename
    print "Filename: " + filename
    print "<br />"

    (fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
    fn=hash(fileitem.file);
    savePath = os.path.join(saveDir, str(fn) + ext)

    open(savePath, 'wb').write(fileitem.file.read())
    cmd = ["identify",savePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    try:
        ext1 = out.split(' ')[1]
    except: 
        print "It's not a photo. Please check the real content."
        cmd = ["rm","-f",savePath]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print '<a href="../index.html">BACK TO INDEX</a>'
        print '</body></html>'
        exit()
    if (ext1 != "JPEG" and ext1 != "PNG" and ext1 != "GIF"):
        print "Please upload a photo(with type JPEG PNG or GIF only)."
        cmd = ["rm","-f",savePath]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        print 'The photo type is: %s <br />' % (out.split()[1])
        filename=str(fn)+ext
        print 'Upload successful. <img src="%s" />'% (os.path.join(readDir, filename))
        print "<br />"
        print '<a href="editor.cgi?fn=%s">Edit Photo</a>' % (filename)
        print "<br />"
    print '<a href="../index.html">Back</a>'
print '</body></html>'