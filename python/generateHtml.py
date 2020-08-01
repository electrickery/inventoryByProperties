#!/usr/bin/python
#

import sys
from libGenerateHtml import *

dir = "."
extensions = [".properties"]
patterns = [".+_[[0-9A-Za-z]{6}$"]

localPath = "../JaakSite/"

refDir = "../JaakSite/ref/"

siteHost = "http://jaaks.be"
sitePath = "/inventaris/"


################################################################################

if len(sys.argv) > 1:
    dir = sys.argv[1]

print (dir)

fileList = findFiles(dir, extensions, patterns)

print()

for propFile in fileList:
    print (propFile)
    
   # generateRefFile(refDir, siteHost + sitePath, propFile)

    generateObjectPage(propFile)
