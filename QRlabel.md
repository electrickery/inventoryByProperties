Onderwerp: via commands een label met QR code en text ontwerpen, te printen met labelprinter Brother QL-700.

Waarom? Voor een hardware inventariseringsproject willen we op zoveel mogelijk geautomatiseerde wijze etiketten maken om objecten te labelen. De labels moeten via een barcode reader snelle toegang geven tot de objectbeschrijving zoals die online zal staan.

Brother heeft een raster API gepubliceerd voor de QL reeks. Met Python package `brother_ql` van  Philipp Klaus kunnen raster bestanden geprint worden via commands en zonder driver, op alle platforms.

---

#### onderwerpen

* Brother QL-700 label info
* QR code specificaties
* qrencode command
* text toevoegen met imagemagick toevoegen
* printen met brother_ql
* te doen: alle commands in een script

---

## Brother QL-700 label info


Voor de Brother QL-700 bestaan labels en continuous tape. Met gebruik van de `brother_ql` command moet de aangeleverde pixel size exact gelijk zijn aan de printable area. Veel gebruikte formaten:

* labels 29x90mm, 
printable area 306x991 pixels = 25.9x83.9 mm 

* tape 62mm,
printable breedte 696 pixels = 58.9 mm

Het navolgende gaat uit van 62mm tape maar we proberen de afmeting van de QR code compatibel te houden met de 29mm labels.


## QR code specs

Version 3 heeft 29x29 QRdots (genaamd modules). Dit is geschikt om niet te lange URL's in te coderen met optimaal correction level. Elke version hoger heeft 4 modules meer. Correction levels bij version 3 geven in theorie de volgende ruimte:

- level L 77 alfanumerieke karakters
- level M 61 alfanumerieke karakters
- level Q 47 alfanumerieke karakters
- level H 35 alfanumerieke karakters

Compleet overzicht van version/level combinaties op:

www.qrcode.com/en/about/version.html

Maar let op: in de praktijk lukt het niet om met `qrencode` zoveel karakters in de code te krijgen! Daarom is het veiliger om version 4 (met 33 modules) te gebruiken als je een consistente afmeting wil hebben.


## qrencode


We willen een QR code met 33 modules (version 4) genereren op maximaal 306 pixels zodat het eventueel op de printable area van de smalle labels past. Er blijft buiten de printable area genoeg marge over die de QR code nodig heeft om leesbaar te zijn.

Met 9 print-pixels per module kom je op 297 pixels. Het is niet mogelijk om exact op 306 pixels uit te komen. Voorbeeld (lange en korte versie van hetzelfde):

    qrencode --level=H --symversion=4 --margin=0 --size=9 --dpi=300 --output=qr.png 'www.katjaas.nl'

    qrencode -l H -v 4 -m 0 -s 9 -d 300 -o qr.png 'www.katjaas.nl'



    --level=H: correction level (L M Q H, default is L)
    --size=9: size of QRdot in printpixels (default is 3)
    --symversion=4 (QR versie, hoger is meer QRdots, default is auto)
    --margin=0: margin in QRdots (default is 4)
    --dpi=300: printer resolution  (default is 72)
    --output=qr.png: output plaatje
    'www.katjaas.nl': de te coderen string


## tekst toevoegen

Op hetzelfde label willen we ook human-readable tekst erbij voor de URL en misschien nog andere dingen. De aangewezen command line tool hiervoor is imagemagick's `convert`.

www.imagemagick.org/Usage/crop/#extent
www.imagemagick.org/Usage/text/#annotate

Eerst moet er wat ruimte aan het QR plaatje geplakt worden om tot de uiteindelijke labelmaat te komen. Voor de continuous tape ligt de labelbreedte vast op 696 pixels. De hoogte van de QR afbeelding kan gehandhaafd blijven want de printer voegt zelf marges toe bij het afsnijden. Dus 696x297 pixels. Het QR plaatje moet links liggen. Daarna plakken we met "convert annotate" de tekst erop.

    convert qr.png -gravity west -extent 696x297 label.png \
    && convert -pointsize 40 -annotate +320+30 'www.katjaas.nl' label.png label.png

Een lange URL moet in meerdere regels opgedeeld worden. Opdelen kan met de newline operator maar dan heb je geen controle over de regelafstand en komt het nogal dicht op elkaar. Het kan beter met aparte argumenten doorgegeven worden. Alle voorgaande commands aan elkaar geknoopt en nu van begin tot eind op dezelfde filename zodat alleen het eindresultaat opgeslagen blijft:

    qrencode -l H -v 4 -m 0 -s 9 -d 300 -o label.png 'www.katjaas.nl/DIYmic/DIYmic.html' \
    && convert label.png -gravity west -extent 696x297 label.png \
    && convert label.png -pointsize 40 -annotate +320+30 'www.katjaas.nl/' \
    -annotate +320+80 'DIYmic/DIYmic.html' label.png


## printen

Voor installatie van `brother_ql` volg de complete instructies op de repository:

https://github.com/pklaus/brother_ql

Mogelijk moet `pip` aangeroepen worden als `pip3`.

Voor het printen eerst met command `lsusb` uitzoeken op welke USB poort de printer zit. Bijvoorbeeld poort 04f9:2042, en met de continuous rol van 62 mm breed:

    brother_ql -m QL-700 -p usb://04f9:2042 -b pyusb print -l 62 label.png


## te doen: script

Doel van het werken via command line is om het hele traject van ontwerpen en printen te automatiseren zodat de invoer van een URL met object record voldoende is om een label uit de printer te laten rollen. Daarom moet dit in een script komen. Vooralsnog is dit een shell script.

	#!/bin/sh
	#
	
	# ID is the generated 6-character identifier
	# ITEM is the concatenation of three property fields: manufacturer, model and identifier.
	# CATEGORY is the type of object, i.e. the directory in which it is placed. 
	
	# qrencode generates a QRcode PNG image from the URL string, Convert creates a larger image,
	# suitable for the brother printer with the QRcode, the URL and ITEM texts. The CATEGORY text 
	# is optional
	
	
	ID=$1
	ITEM=$2
	CATEGORY=$3
	URL="http://jaakbartok.be/ref/${ID}.html"
	IMAGE=${ID}.png
	
	
	qrencode -l H -v 4 -m 0 -s 7 -d 300 -o ${IMAGE} ${URL} \
	&& convert ${IMAGE} -gravity north-west -extent 696x297 \
 	-pointsize 30 -annotate +5+255 ${URL} \
 	-annotate +270+0 "${ITEM}" \
 	-annotate +270+30 "${CATEGORY}" \
 	${IMAGE}
	
	~/.local/bin/brother_ql -m QL-700 -p usb://04f9:2042 -b pyusb print -l 62 ${IMAGE}


