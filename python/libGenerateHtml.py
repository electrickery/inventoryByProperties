#!/usr/bin/python
# library functions for generate html from properties

import os
import re
import datetime

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
        if os.path.isdir(completePath):
            completeFileList = completeFileList + getFiles(completePath)
        else:
            completeFileList.append(completePath)
    return completeFileList


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
    return (now.strftime("%Y-%M-%d %H:%M:%S")) 

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
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Redirecting to %%OBJECTURL%%</p>
    </body>
</html>"""

#    print (refDir, sitePrefix, propFile)
    siteDirs = getDirs(propFile).replace(localPath, "")
    siteObjectHtmlFileName = sitePrefix + siteDirs + getFileNameBase(propFile) + ".html"
    localRefFileName = refDir + getFileNameBase(propFile) + ".html"
#    print ("obj: " + siteObjectHtmlFileName)
#    print ("ref: " + localRefFileName)
    
    refFile = open(localRefFileName, 'w')
    refFile.write(refHtmlTemplate.replace("%%OBJECTURL%%", siteObjectHtmlFileName))
    refFile.close()
    
def createMetadataSection(props):
    metadataTableTemplate = """<p><table>
%%METADATAROWSET%%        </table></p>"""

    metadataRowSetTemplate = """            <tr><td>%%KEY%%</td> <td>%%VALUE%%</td></tr>
"""
    metadataRowSet = ""
    for propKey in props.keys():
#        print (propKey + " - " + props[propKey])
        metadataRowSet += metadataRowSetTemplate.replace("%%KEY%%", propKey).replace("%%VALUE%%", props[propKey])
    
    return metadataTableTemplate.replace("%%METADATAROWSET%%", metadataRowSet)
    
def generateObjectPage(propFile):
    objectHtmlTemplate = """<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'
'http://www.w3.org/TR/html4/strict.dtd'> 
<html>
    <head>
        <title>%%TITLE%%</title>
        <link rel='stylesheet' type='text/css' href='/css/table.css'>
        <meta charset="UTF-8">
    </head>
    <body>
        <h2>%%NAME%%</h2>
        %%METADATA%%
%%IMAGES%%
%%COMMENTS%%
        <p><i>Latest update: %%DATE%%</i></p>
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
                                    .replace("%%METADATA%%", metadataSection)\
                                    .replace("%%IMAGES%%", imageSection)\
                                    .replace("%%COMMENTS%%", commentSection)

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
