# Inventory by Property files

This is a Proof of Concept of a HTML generator based on propery files. The reason 
to create it is a request by a non-programmer to create an on-line inventory of
a large collection of computer and electronic objects. 

As most maintenance is expected to be performed by a non-programmer or information
specialist, the data-basis is kept to the absolute minimum. All information is
stored in three types of files:

* *.properties file for the object metadata
* *.[jpg|png|gif] for images of the object
* *.txt for additional textual information on the object
    
The filenames have additional structure: "*_XXXXXX.ext", where XXXXXX is a 
system-unique hexadecimal number shared by the one metadata file, all the images 
and one or more comment files. The part before the "_XXXXXX" is free, but it is
encouraged to use the brand and model/type of the object, separated by underscores.
All files referring to the same object are expected in the same directory. 
The organisation of the directory tree is not fixed, with as only exception a 'ref'
directory, used for a passive redirect level.

The functional complete version of the generating code is written in Pyton, 
compatible with 2.x and 3.6; the original prototype is written in Perl5.

The main content-generating file is generateHtmlFiles.py, which generates four
types of files:

* an HTML object-file with the same name as the object metadata file containing
  all information of the metadata file, references of the images and the
  content of the comment files. This file will be written in the same directory 
  as the source documents,
* an HTML file in the 'ref' directory containing a redirect to the HTML 
  object-file. This allows for fixed URLs, independent of the actual location
  of the files in the tree. The intention is to create QRCode labels attached
  to the physical object,
* a set of category-index files, one for each category,
* an HTML index file in the ref directory listing all objects in all categories.
  
The 'theNumber.txt' file is part of the identifier and label generator, 
which is not finished.

The Perl version can be started from just above the perl directory, the Python
version has to be run from the python directory.

   
    python3 python/generateHtml.py root/

      
F.J. Kraan, 2020-08-09
      
