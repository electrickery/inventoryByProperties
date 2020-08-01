#!
#

import sys
from libGenerateHtml import *
dir = "."

if len(sys.argv) > 1:
    dir = sys.argv[1]

indexFileName = dir + "/index.html"

indexPrefixTemplate = """<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
<html>
    <head>
        <title>%%TITLE%%</title>
    </head>
    <body>
        <h2>%%TITLE%%</h2>
        <p><ul>
"""

indexPostfixTemplate = """        </ul></p>
        <p>Last updated: %%DATESTAMP%%</p>
    </body>
</html>"""

indexLineTemplate = """           <li><a href='%%FILENAME%%'>%%FILENAMEBASE%%</a></li>
"""


files = findFiles(dir, [".html"], ['.+_[[0-9A-Za-z]{6}$'])

indexFile = open(indexFileName, 'w')

title = dir
indexFile.write (indexPrefixTemplate.replace("%%TITLE%%", title))

for pathFile in sorted(files):
    fileName = getFileName(pathFile)
    fileNameBase = getFileNameBase(pathFile)
    indexFile.write (indexLineTemplate.replace("%%FILENAMEBASE%%", fileNameBase).replace("%%FILENAME%%", fileName))
    
indexFile.write (indexPostfixTemplate.replace("%%DATESTAMP%%", getCurrentTime()))

indexFile.close()
