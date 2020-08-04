#!/usr/bin/python
#

import sys

from libGenerateHtml import *


def createObjectFile(dirBase, objectProps):
    fileName = "_".join([objectProps["fabrikant"], objectProps["model"]])
    if ("name" in objectProps):
        "_".join([fileName, objectProps["name"]])
    fileName = dirBase + "/" + sanitizeString(fileName) + "_" + getNextNumber() + ".properties"

    print ("fileName: " + fileName)
    file = open(fileName, 'w')
    for propKey in objectProps.keys():
        print (propKey + " = " + objectProps[propKey])
        file.write(propKey + " = " + objectProps[propKey] + "\n")
    file.close()
            


numFile = "../theNumber.txt"
csvFile = ""

targetDirBase = "../JaakSite"

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
        objectProps = {}
        fields = line.split(";")
        for i in range(headerCount):
#            print (headers[i] + " = " + fields[i])
            objectProps[headers[i]] = fields[i]

        createObjectFile(targetDir, objectProps)
