#!/usr/bin/env python

import os
import sys
import cgi
import cgitb
import glob
import subprocess
import urlparse


print 'Content-type: text/html\n'

saveDir = '/var/www/html/myupload' # Full path or relative path
readDir = '/myupload'

cgitb.enable()

form = cgi.FieldStorage()

print '<html><body>'
url = os.environ["REQUEST_URI"] 
try:
    url = url.split("=")[1]
except:
    print "No file selected."
    print '<a href="../index.html">Index</a>'
    print "</body></html>"
    exit()
if  not (os.path.isfile(saveDir + "/" + url)):
    print "No such a file"
    print '<a href="../index.html">Index</a>'
    print "</body></html>"
    exit()
ext = url.split(".")[1]
ext = '.' + ext
fn = url
fn_new = str(int(url.split('.')[0]) + 1) + '.' + url.split('.')[1]
original = True
if ('top' in form):
    cmd = ['convert', \
            (saveDir + '/' + url),\
            '-background', 'White', '-pointsize', form['fontsize'].value, \
            '-font', form['fonttype'].value, \
            'label:'+form['annotateMsg'].value, '+swap', \
            '-gravity', 'center', '-append', \
            (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False

if ('bottom' in form):
    cmd = ['convert', \
            (saveDir + '/' + url),\
            '-background', 'White', '-pointsize', form['fontsize'].value, \
            '-font', form['fonttype'].value, \
            'label:'+form['annotateMsg'].value, \
            '-gravity', 'center', '-append', \
            (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False

if ('border' in form):
    cmd = ['convert', \
            (saveDir + '/' + url),\
            '-bordercolor', 'Black', '-border', '10', \
            (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False


if ('lomo' in form):
    cmd = ['convert', \
            (saveDir + '/' + url),\
            '-channel', 'R', '-level', '33%', '-channel', 'G', 'level', '33%', \
            (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False

if ('blur' in form):
    cmd = ['convert', (saveDir + '/' + url), '-blur', '0.5x2', (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False


def getImageWidth(imagePath):
    cmd = ['identify', imagePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    return ((out.split()[2]).split('x')[0])

def getImageHeight(imagePath):
    cmd = ['identify', imagePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    return ((out.split()[2]).split('x')[1])

if ('lensflare' in form):
    cmd = ['convert', 'lensflare.png', '-resize', \
            getImageWidth((saveDir + '/' + url))+'x' + getImageHeight((saveDir + '/' + url))+'!' , 'tmp.png']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()

    cmd = ['composite', '-compose', 'screen', '-gravity', 'northwest', 'tmp.png', \
            (saveDir + '/' + url), (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False

if ('bw' in form):
    cmd = ['convert', (saveDir + '/' + url), '-type', 'grayscale', 'a'+ext]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()

    cmd = ['convert', 'bwgrad.png', '-resize', \
            getImageWidth((saveDir + '/' + url))+'x'+getImageHeight((saveDir + '/' + url))+'!', \
            'tmp.png']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()

    cmd = ['composite', '-compose', 'softlight', '-gravity', 'center', 'tmp.png', \
            'a'+ext, \
            (saveDir + '/' + fn_new)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    original=False

if ('undo' in form):
    fn_test=str(int(fn.split('.')[0]) - 1) + '.' + fn.split('.')[1]
    if(os.path.isfile((saveDir + '/' + fn_test))):
        cmd = ['rm', (saveDir + '/' + fn)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        fn=str(int(url.split('.')[0]) - 1) + '.' + url.split('.')[1]
        url = fn
    else:
        print "<br/>That's your original photo.<br/>"

if ('discard' in form):
    fn_new=str(int(fn.split('.')[0]) - 1) + '.' + fn.split('.')[1]
    while (os.path.isfile((saveDir + '/' + fn_new))):
        cmd = ['rm', (saveDir + '/' + fn)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        fn=fn_new
        fn_new=str(int(fn.split('.')[0]) - 1) + '.' + fn.split('.')[1]
    print '<a href="../index.html">Index</a>'
    url = fn

if ('finish' in form):
    cmd = ['cp',(saveDir + '/' + fn),("/var/www/html/newphoto/")+fn]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    print '<br/><img src="%s" style="max-width:500px;max-height:500px;" /><br/>' % (readDir + "/" + url)
    host = os.environ["HTTP_HOST"]
    print (host + os.path.abspath(readDir + "/" + url))
    print '<br/><a href="../index.html">Index</a>'
    print "</body></html>"
    exit()

url = readDir + "/" + url

print '<img src="%s" style="max-width:500px;max-height:500px;" />' % url
print '<br /> Original Photo <br />'
if not original:
    print '<br/><img src="%s" style="max-width:500px;max-height:500px;" />' % (readDir + "/" + fn_new)
    print '<br /> Modified Photo <br />'

if not original:
    fn = fn_new

print '<td>'
print '<br/>'
print '<form action="editor.cgi?fn=%s" method="POST">Annotate <input type="text" placeholder="Please input your want..."name="annotateMsg" required="required"><br />' % fn
print '''
Font Type <select name='fonttype'>
<option value='Times-Roman'>Times-Roman</option>
<option value='Courier'>Courier</option>
<option value='Helvetica'>Helvetica</option>
</select>
<br />
'''
print '''
Font Size <select name='fontsize'>
'''
for i in range(10, 49):
    print '''<option value="%d">%d</option>'''%(i, i)

print '</select><br />'

print '''
<input type="submit" value="Annotate Top" name="top">
'''
print '''
<input type="submit" value="Annotate Bottom" name="bottom">
</form>
'''

print '<table style="width:100%">'
print '<tr>'

print 'Filters'

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Border" name="border">
</form>
''' 

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Lomo" name="lomo">
</form>
'''

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Lens Flare" name="lensflare">
</form>
'''

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Black & White" name="bw">
</form>
'''

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Blur" name="blur">
</form>
'''

print '</tr>'
print '<br/><br/>Operations:'
print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Undo" name="undo">
</form>
'''

print '<form action="../index.html" method="POST">' 
print '''
<input type="submit" value="Discard" name="discard">
</form>
'''

print '<form action="editor.cgi?fn=%s" method="POST">' % fn
print '''
<input type="submit" value="Finish" name="finish">
</form>
'''

print "</body></html>"