#!/usr/bin/python
#

#file = open('sample.txt', 'w')


def getNextNumber():
    numberFile = "theNumber.txt"
    
    file = open(numberFile, 'r')
    count = int(file.readline().rstrip(), 16)
    file.close()
    
    count = count + 1
    
    file = open(numberFile, 'w')
    file.write(hex(count))
    file.close()
    
getNextNumber()
