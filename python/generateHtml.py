#!/usr/bin/python
#

################################################################################
# generateHtml.py - a script to generate HTML files from property files and
#  a navigation structure for these HTML files. Next to the normal directory
#  hierarchy, an indexing file is generated allowing short URLs to be used for
#  navigation from QR-codes.
#
# The primary goal was to create a low-tech approach to making an object 
# inventory available online.
################################################################################

#!/usr/bin/python
# -*- coding: latin-1 -*-
# library functions for generate html from properties

import os
import re
import datetime
import sys

version = "1.0"
script  = "generateInventory.py"

################################################################################


def findFiles(base, extensions, filters):
    allList = getFiles(base)
    filtList = []
    for item in allList:
        if selector(item, extensions, filters):
            filtList.append(item)
    return filtList
    
def selector(item, extensions, filters):
    splitItem = os.path.splitext(item)
    base = os.path.splitext(item)[0]
    ext  = os.path.splitext(item)[1]
#    print ("selector: " + base + " . " + ext)
    if extensions:
        if not ext in extensions:
##            print (" not in extensions: " + item)
            return False
##        else:
##            print (" in extensions: " + item  )
    if filters:
        found = False
        for filterPatt in  filters:
#            print (" filt. " + filterPatt + " : " + base)
            if re.match(filterPatt, base):
#                print ("  match: " + item)
                found = True
        return found
    return True


def getFiles(dirName):
    listOfFile = os.listdir(dirName)
    completeFileList = []
    for file in listOfFile:
        completePath = os.path.join(dirName, file)
        if completePath.startswith("./"):
            completePath = completePath[2:]
        if os.path.isdir(completePath):
            completeFileList = completeFileList + getFiles(completePath)
        else:
            completeFileList.append(completePath)
    return completeFileList

def getDirectories(dirName):
    listOfDirs = os.listdir(dirName)
    completeDirList = []
    for dir in listOfDirs:
#        print ("gds: " + dirName + " | " + dir)
        completePath = os.path.join(dirName, dir)
        if os.path.isdir(completePath):
            completeDirList.append(completePath)
    return completeDirList

def getNextNumber():
    numberFile = "../theNumber.txt"
    
    file = open(numberFile, 'r')
    count = int(file.readline().rstrip(), 16)
    file.close()
    
    count = count + 1
    
    file = open(numberFile, 'w')
    file.write(hex(count))
    file.close()
    return (str(count))

def getCurrentTime():
    now = datetime.datetime.now()
    return (now.strftime("%Y-%m-%d %H:%M:%S")) 

def getDirs(path):
    return os.path.dirname(path) + "/"
    
def getFileName(path):
    return os.path.basename(path)

def getFileNameBase(path):
    return os.path.splitext(os.path.basename(path))[0]
    
def getFileNameExtension(path):
    return os.path.splitext(path)[1]

def getProperties(propFile):
    props = {}   
    file = open(propFile, 'r')

    lines = file.readlines()
    for line in lines:
        if (not line.strip() or line.startswith("#")):
            continue
        line = line.rstrip()
        if (re.match("^\W*", line)):
            (key, value) = re.split("\w*=\w*", line)
            props[key.strip()] =  value.strip()
        
    file.close()
    return props


def generateRefFile(refDir, sitePrefix, propFile, localPath):
    refHtmlTemplate = """<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'
'http://www.w3.org/TR/html4/strict.dtd''> 
<html>
    <head>
        <meta http-equiv='Refresh' content=\"0; url='%%OBJECTURL%%'\" />
    </head>
    <body>
        <p>Redirecting to <a href='%%OBJECTURL%%'>%%OBJECTURL%%</a></p>
    </body>
</html>"""

#    print (refDir, sitePrefix, propFile)
    siteDirs = getDirs(propFile).replace(localPath, "")
    siteObjectHtmlFileName = sitePrefix + siteDirs + getFileNameBase(propFile) + ".html"
    localRefFileName = refDir + getIdFromFilename(propFile) + ".html"
#    print ("obj: " + siteObjectHtmlFileName)
#    print ("ref: " + localRefFileName)
    print (localRefFileName)
    refFile = open(localRefFileName, 'w')
    refFile.write(refHtmlTemplate.replace("%%OBJECTURL%%", siteObjectHtmlFileName))
    refFile.close()
    
def createMetadataSection(props):
    metadataTableTemplate = """<p><table><tbody>
%%METADATAROWSET%%        </tbody></table></p>"""

    metadataRowSetTemplate = """            <tr><td>%%KEY%%</td> <td>%%VALUE%%</td></tr>
"""
    metadataRowSet = ""
    for propKey in props.keys():
#        print (propKey + " - " + props[propKey])
        metadataRowSet += metadataRowSetTemplate.replace("%%KEY%%", propKey).replace("%%VALUE%%", props[propKey])
    
    return metadataTableTemplate.replace("%%METADATAROWSET%%", metadataRowSet)
    
def generateObjectPage(propFile):
    global version
    global script
    objectHtmlTemplate = """<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'
'http://www.w3.org/TR/html4/strict.dtd'> 
<html>
    <head>
        <title>%%TITLE%%</title>
        <link rel='stylesheet' type='text/css' href='../../css/inventaris.css'>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charset="UTF-8">
    </head>
    <body>
        <header>
            <iframe class="header" src="../header.html" target="_parent"></iframe>
        </header>
    
        <h2>%%NAME%%</h2>
        %%METADATA%%
%%IMAGES%%
%%COMMENTS%%
        <p><i>Latest update: %%DATE%% - Generated by: %%SCRIPT%%, %%VERSION%%</i></p>
        <!-- generateObjectPage -->
    </body>
</html>"""

    localObjectHtmlFileName = getDirs(propFile) + getFileNameBase(propFile) + ".html"
    
    props = getProperties(propFile)
    
    title = propFile
    
#    for propKey in props.keys():
#        print (propKey + " - " + props[propKey])

    name =  getDirs(propFile) + " - " + props["fabrikant"] + " " + props["model"]
    if ("naam" in props):
         name = name + " " + props["naam"]
        
    date = getCurrentTime()
    
    metadataSection = createMetadataSection(props)
    imageSection = createImageSection(propFile)
    commentSection = createCommentSection(propFile)
    
    objectHtml = objectHtmlTemplate.replace("%%TITLE%%", title)\
                                    .replace("%%NAME%%", name)\
                                    .replace("%%DATE%%", date)\
                                    .replace("%%SCRIPT%%", script)\
                                    .replace("%%VERSION%%", version)\
                                    .replace("%%METADATA%%", metadataSection)\
                                    .replace("%%IMAGES%%", imageSection)\
                                    .replace("%%COMMENTS%%", commentSection)

    print (localObjectHtmlFileName)
    file = open(localObjectHtmlFileName, 'w')
    file.write(objectHtml)
    file.close()
    

def createImageSection(propFile):
    imagesTemplate = """        <p><img src='%%IMAGE%%'/></p>
"""
    id = getIdFromFilename(propFile)
    idPatterns = [ ".+_(" + id + ")$" ]
    extensions = [ ".gif", ".jpg", ".png" ]
    dir = getDirs(propFile)
    
    imageFileList = findFiles(dir, extensions, idPatterns)
    
    imageSection = ""
    for image in imageFileList:
        imageSection += imagesTemplate.replace("%%IMAGE%%", getFileName(image))
        
    return imageSection

def createCommentSection(propFile):
    commentsHeader = """        <h3>Comments</h3>
"""

    commentTemplate = """        <p>%%COMMENT%%</p>
"""
    
    id = getIdFromFilename(propFile)
    idPatterns = [ ".+_(" + id + ")$" ]
    extensions = [ ".txt" ]
    dir = getDirs(propFile)
    
    commentFileList = findFiles(dir, extensions, idPatterns)
    
    commentsSection = ""
    if (commentFileList):
        commentsSection = commentsHeader
    
    for commentFile in commentFileList:
        file = open(commentFile, 'r')
        lines = file.readlines()
        file.close()
        for line in lines:
            if (line.strip()):
                commentLine = commentTemplate.replace("%%COMMENT%%", line.rstrip())
                commentsSection += commentLine
    return commentsSection

def generateRefIndex(fileList, localRefDir):
    global version
    global script
    refIndexTemplate = """<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'
'http://www.w3.org/TR/html4/strict.dtd'> 
<html>
    <head>
        <title>%%TITLE%%</title>
        <link rel='stylesheet' type='text/css' href='/css/inventaris.css'>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charset="UTF-8">
    </head>
    <body>
        <header>
            <iframe class="header" src="/inventaris/header.html" target="_parent"></iframe>
        </header>

        <h2>%%NAME%%</h2>
        <p><ul>
%%REFFILES%%
        </ul></p>
        <p><i>Latest update: %%DATE%% - Generated by: generateHtml.py, %%VERSION%%</i></p>
        <!-- generateRefIndex -->
    </body>
</html>    
"""  
    refIndexLineTemplate = "            <li><a href='%%REFURL%%'>%%REFNAME%%</a></li>"
    
    refIndexLines = []
    for file in fileList:
        refUrl = getIdFromFilename(file) + ".html"
        refName = getFileNameBase(file)
        refIndexLines.append(refIndexLineTemplate.replace("%%REFNAME%%", refName).replace("%%REFURL%%", refUrl))
        
    refIndexFileSection = '\n'.join(refIndexLines)
    
    refIndex = refIndexTemplate.replace("%%TITLE%%", "Complete inventaris")\
                               .replace("%%NAME%%", "Complete inventaris")\
                               .replace("%%REFFILES%%", refIndexFileSection)\
                               .replace("%%DATE%%", getCurrentTime())\
                               .replace("%%SCRIPT%%", script)\
                               .replace("%%VERSION%%", version)
    
    refIndexName = localRefDir + "index.html"
    print (refIndexName)
    file = open(refIndexName, 'w')
    file.write(refIndex)
    file.close()
    
def getCategorieIndex(dir, subDirList):
    global version
    global script
    indexFileName = dir + "/index.html"
    
    indexTemplate = """<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
    <html>
        <head>
            <title>%%TITLE%%</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link rel="stylesheet" type="text/css" href="../css/inventaris.css">
        </head>
        <body>
        <header>
            <iframe class="header" src="header.html" target="_parent"></iframe>
        </header>
        <h2>%%TITLE%%</h2>
            <nav>
%%CATEGORYLINES%%
            </nav>
            <p>Last updated: %%DATESTAMP%% - Generated by: %%SCRIPT%%, %%VERSION%%</p>
            <!-- getCategorieIndex -->
        </body>
    </html>"""

    indexLineTemplate = "                <p><a href='%%FILENAME%%'>%%FILENAMEBASE%%</a></p>"
    
    title = dir

    categoryLines = []
    for pathFile in sorted(subDirList):
        fileName = getFileName(pathFile)
        fileNameBase = getFileNameBase(pathFile)
        categoryLines.append(indexLineTemplate.replace("%%FILENAMEBASE%%", fileNameBase)\
                                              .replace("%%FILENAME%%", fileName))
    categoryLines.append(indexLineTemplate.replace("%%FILENAMEBASE%%", "alles")\
                                          .replace("%%FILENAME%%", "../ref/index.html"))    
    
    print (indexFileName)
    indexFile = open(indexFileName, 'w')
    indexFile.write (indexTemplate.replace("%%TITLE%%", title)\
                                  .replace("%%CATEGORYLINES%%", "\n".join(categoryLines))\
                                  .replace("%%DATESTAMP%%", getCurrentTime())\
                                  .replace("%%VERSION%%", version)\
                                  .replace("%%SCRIPT%%", script))

    indexFile.close()
    
def genObjectIndex(dir):
    global version
    global script
    indexFileName = dir + "/index.html"

    indexTemplate = """<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
    <html>
        <head>
            <title>%%TITLE%%</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link rel="stylesheet" type="text/css" href="../../css/inventaris.css">
        </head>
        <body>
            <header>
                <iframe class="header" src="../header.html" target="_parent"></iframe>
            </header>
            <h2>%%TITLE%%</h2>
            <p>U kunt hieronder virtueel snuffelen in Jaak's hardware verzameling. Let wel, de 
            inventarisatie is nog lang niet compleet.</p>
            <nav>
%%INDEXLINES%%
            </nav>
            <p>Last updated: %%DATESTAMP%% - Generated by: %%SCRIPT%%, %%VERSION%%</p>
            <!-- genObjectIndex -->
        </body>
    </html>"""

    indexLineTemplate = "           <p><a href='%%FILENAME%%'>%%FILENAMEBASE%%</a></p>"

    files = findFiles(dir, [".html"], ['.+_[[0-9A-Za-z]{6}$'])

    indexLines = []
    for pathFile in sorted(files):
        fileName = getFileName(pathFile)
        fileNameBase = getFileNameBase(pathFile)
        indexLines.append(indexLineTemplate.replace("%%FILENAMEBASE%%", fileNameBase)\
                                          .replace("%%FILENAME%%", fileName))
        
    print (indexFileName)
    indexFile = open(indexFileName, 'w')

    title = dir
    indexFile.write (indexTemplate.replace("%%TITLE%%", title)\
                                  .replace("%%INDEXLINES%%", "\n".join(indexLines))\
                                  .replace("%%DATESTAMP%%", getCurrentTime())\
                                  .replace("%%VERSION%%", version)\
                                  .replace("%%SCRIPT%%", script))
    indexFile.close()

def getIdFromFilename(propFile):
    id = ""
    idPattern = '.+_([0-9A-Za-z]{6})\.'
    idFound = re.match(idPattern, propFile)
    if idFound:
        id = (idFound.group(1))
    return id

def sanitizeString(name):
    #[\|\/:;=\$\!\@\#%\^\&\*\(\)\[\]]
    return re.sub("[\|\/:;=\$\!\@\#%\^\&\*\(\)\[\]\s]", "_", name)


################################################################################


dir = "."
extensions = [".properties"]
patterns = [".+_[[0-9A-Za-z]{6}$"]

localPath = "../root/"

localRefDir = "../root/ref/"

#siteHost = "http://jaakbartok.be/"
sitePath = "/inventaris/"
siteRefPath = "/ref/"



if len(sys.argv) > 1:
    dir = sys.argv[1]

print (dir)

originalDir = os.getcwd()
os.chdir(dir);

print()

fileList = findFiles(".", extensions, patterns)

for propFile in fileList:
    
    generateRefFile(localRefDir, "../", propFile, localPath)

    generateObjectPage(propFile)
    
print()

generateRefIndex(fileList, localRefDir)

os.chdir(originalDir);

print()

inventDir = "inventaris"

os.chdir(dir);
subDirList = getDirectories(inventDir)
for subDir in subDirList:
    
    genObjectIndex(subDir)

getCategorieIndex(inventDir, subDirList)
os.chdir(originalDir)
