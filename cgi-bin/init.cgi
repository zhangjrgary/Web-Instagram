#!/usr/bin/env python

import os
import cgi
import cgitb
import subprocess
import sys

print "Content-Type: text/html\n\n"

print "<head>"
print '<link rel="stylesheet" href="http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css">'
print "<body>"

cmd=["rm",'-rf','/var/www/html/myupload/']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()
print err
cmd=["rm",'-rf','/var/www/html/newphoto/']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()
cmd=['mkdir','/var/www/html/newphoto/']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()
cmd=['mkdir','/var/www/html/myupload/']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = p.communicate()
print "<h1>The system is initialized ~</h1>"
print
print '<a  href="../index.html">Back</a>'
#print '<input class="nav nav-pills" type=button value="Index Page" onclick="window.open(".")" />'
print "</head></body>"