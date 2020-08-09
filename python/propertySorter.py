#!/usr/bin/python
#
# propertySorter

import sys
from libGenerateHtml import *

dir = "."
extensions = [".properties"]
patterns = [".+_[[0-9A-Za-z]{6}$"]

localPath = "../root/"

localRefDir = "../root/ref/"

#siteHost = "http://jaakbartok.be/"
sitePath = "/inventaris/"
siteRefPath = "/ref/"

# portables: id;fabrikant;model;Type ;S/N;org op system;product key;aktueel  op sys office ;opm ;locatie;processor;servicce tag;proc;ram;disk
# boards:    id;vorm;fabrikant;model;processor;jaar;onBoard;Chipset
# IBM:       id;fabrikant;nr;model;board;date b;rom;video /par;floppy controllrer;HD controller ;bay 1;bay1u;bay2;bay2u
# ideHarddisks: id;fabrikant;model;code;serienummer;geometrie;opmerkingen


propertyOrder = ["id", "fabrikant", "model", "naam", "nr", "vorm", "Type-", "locatie", "org-op-system", "product-key", "aktueel-op-sys-office-", \
 "opm ", "locatie", "servicce-tag", "proc", "processor", "ram", "disk", "jaar", "onBoard", "Chipset", "board", "date b", \
 "rom", "video /par", "floppy-controllrer", "HD-controller-", "bay-1", "bay1u", "bay2", "bay2u", "code", "serienummer", "geometrie", "opmerkingen"]
#propertyOrder = ["id", "fabrikant", "model", "naam", "vorm", "type", "locatie", "org-OS", "actuel-OS", "S/N", "product-key", "opm", \
# "opmerkingen", "processor", "service-tag", "ram", "disk", "jaar", "onBoard", "chipset", "code", "serienummer", "geometrie", "nr", "board", "date-bios", "rom", "video-par", "floppy-controller", "HD-controller", "bay1", "bay1u", "bay2", "bay2u" ]

################################################################################


if len(sys.argv) > 1:
    dir = sys.argv[1]

print (dir)

originalDir = os.getcwd()
os.chdir(dir);

print()

fileList = findFiles(".", extensions, patterns)

for fileName in fileList:
    print (fileName)

    props = getProperties(fileName)
    
    file = open(fileName, 'w')
    for propKey in propertyOrder:
        if propKey in props:
            cleanPropKey = propKey
            if (propKey.endswith("-")):
                cleanPropKey = propKey[0:-1]
            print ("  " + cleanPropKey + " = " + props[propKey])
            file.write(cleanPropKey + " = " + props[propKey] + "\n")
    file.close()

    
