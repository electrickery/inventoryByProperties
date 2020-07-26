# Inventory by Property files

This is a Proof of Concept of a HTML generator based on propery files. The reason 
to create it is a request by a non-programmer to create an on-line inventory of
a large collection of computer and electronic objects. 

As most maintenance is expected to be performed by a non-programmer or information
specialist, the data-basis is kept to the absolute minimum. All information is
stored in three types of files:

    * *.txt files for the object metadata
    * *.[jpg|png|gif] for images of the object
    * *.comment for additional textual onformation of the object
    
The filenames have additional structure: "*_XXXXXX.ext", where XXXXXX is a 
system-unixte hexadecimal number shared by the one metadata file, all the images 
and one or more comment files. The part before the "_XXXXXX" is free, but it is
encouraged to use the brand and model/type of the object, separated bu underscores.
All files referring to the same object are expected in the same directory, but 
the organisation of the directory tree is not fixed. The only exception is a 'ref'
directory, used for a passive redirect level.

The main content-generating file is perl/generateHtmlFiles.pl, which generates two
files:

    * an HTML object-file with the same name as the object metadata file containing
      all information of the metadata file, references of the images and the
      content of the comment files. This file will be written in the same directory 
      as the source documents,
    * an HTML file in the 'ref' directory containing a redirect to the HTML 
      object-file. This allows for fixed URLs, independent of the actual location
      of the files in the tree. The intention is to create QRCode labels attached
      to the physical object.
      
F.J. Kraan, 2020-07-26
      