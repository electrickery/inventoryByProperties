#!/usr/bin/python
#

import os
import re
import datetime
import sys

def getNextNumber():
    numberFile = "theNumber.txt"
    
    file = open(numberFile, 'r')
    count = int(file.readline().rstrip(), 16)
    file.close()
    
    count = count + 1
    
    file = open(numberFile, 'w')
    file.write(hex(count))
    file.close()
    return (hex(count))[2:]


def createObjectFile(dirBase, objectProps):
    id = getNextNumber()
    fileName = "_".join([objectProps["fabrikant"], objectProps["model"]])
    if ("name" in objectProps):
        "_".join([fileName, objectProps["name"]])
    fileName = dirBase + "/" + sanitizeString(fileName) + "_" + id + ".properties"

    print ("fileName: " + fileName)
    file = open(fileName, 'w')
    print ("id = " + id)
    file.write("id = " + id + "\n")
    for propKey in objectProps.keys():
        if (objectProps[propKey]):
            print (propKey + " = " + objectProps[propKey])
            file.write(propKey + " = " + objectProps[propKey] + "\n")
    file.close()
            
def getFileNameBase(path):
    return os.path.splitext(os.path.basename(path))[0]
    
def sanitizeString(name):
    #[\|\/:;=\$\!\@\#%\^\&\*\(\)\[\]]
    return re.sub("[\|\/:;=\$\!\@\#%\^\&\*\(\)\[\]\s]", "_", name)

################################################################################

csvFile = ""

targetDirBase = "root/inventaris"

if len(sys.argv) > 1:
    csvFile = sys.argv[1]
    
if (not csvFile):
    print ("No csv file specified. Exiting.")
    exit(1)
    
print ("source file: " + csvFile)

targetDir = targetDirBase + "/" + getFileNameBase(csvFile)

print ("target directory: " + targetDir)
    
file = open(csvFile, 'r')
lines = file.readlines()
file.close()

lineCount = 0
headerCount = 0
objectProps = {}
for line in lines:
    lineCount += 1
    line = line.rstrip()
    print (str(lineCount) + "  " + line.rstrip())
    if (lineCount == 1):
        headers = line.split(";")
        headerCount = len(headers)
    else:
        if (line.strip()):
            objectProps = {}
            fields = line.split(";")
            for i in range(headerCount):
                print (headers[i] + " = " + fields[i])
                objectProps[headers[i].strip()] = fields[i].strip()

        createObjectFile(targetDir, objectProps)
