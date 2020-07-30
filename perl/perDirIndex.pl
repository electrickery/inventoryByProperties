#!/usr/bin/perl
use strict;
use warnings;

use Path::Iterator::Rule;
use File::Basename;

our $HTMLEXT = ".html";
our $HTMLPATT = "_([0-9A-F]{6})${HTMLEXT}\$";

our $refDir = "site/ref/";

my @dirs = @ARGV;
if (@dirs == 0) { push(@dirs, "site") };

my @htmlFiles = &getHtmlFiles(@dirs);
print "htmlCount: " . @htmlFiles . "\n";

my $indexName = "$dirs[0]/index.html";
print " $indexName\n";
open OFH, ">$indexName"  or die "$0: error opening \'$indexName\'";

my $indexPrefix = &getIndexPrefixTemplate();
my($name, $dirs, $suffix) =  fileparse($indexName, qr/\.[^.]*/);
$indexPrefix =~ s/%%TITLE%%/$dirs/g;
print OFH $indexPrefix;

foreach my $fileName (@htmlFiles) {
    print " $fileName\n";
    my $indexLine = &getIndexLineTemplate();
    my($name, $dirs, $suffix) =  fileparse($fileName, qr/\.[^.]*/);
    my $localName = $name . $suffix;
    $indexLine =~ s/%%FILENAME%%/$localName/g;
    print OFH $indexLine;
}

my $indexPostfix = &getIndexPostfixTemplate();
my $dateStamp = &getCurrentTime();
$indexPostfix =~ s/%%DATESTAMP%%/$dateStamp/;
print OFH $indexPostfix;

close OFH;

sub getHtmlFiles($$) {
    my (@dirs) = @_;
    my $rule = Path::Iterator::Rule->new;
    my @files;
    for my $fileName ( $rule->all( @dirs ) ) {
        if ($fileName =~ m/$HTMLPATT/i) { # filter files ending with _XXXXXX.properties
            my($name, $dirs, $suffix) =  fileparse($fileName, qr/\.[^.]*/);
            push (@files, $name . $suffix);
        }
    }
    return @files;
}

sub getIndexPrefixTemplate() {
    return "<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
<html>
    <head>
        <title>%%TITLE%%</title>
    </head>
    <body>
        <h2>%%TITLE%%</h2>
        <p><ul>
        ";
}

sub getIndexPostfixTemplate() {
    return "</ul>
        </p>
        <p>Last updated: %%DATESTAMP%%</p>
    </body>
</html>
";
}

sub getIndexLineTemplate() {
     return "       <li><a href='%%FILENAME%%'>%%FILENAME%%</a></li>
     ";
}

sub getCurrentTime() {
    my $currTime = time();
    return time2timeStamp(gmtime($currTime));
}

sub time2timeStamp {
    my @gmTimeArr = @_;
    my $year = $gmTimeArr[5] + 1900;
    my $month = $gmTimeArr[4] + 1;
    $month = substr("0".$month,-2,2);
    my $mday = $gmTimeArr[3];
    $mday = substr("0".$mday,-2,2);
    my $hour = $gmTimeArr[2];
    $hour = substr("0".$hour,-2,2);
    my $minute = $gmTimeArr[1];
    $minute = substr("0".$minute,-2,2);
    my $second = $gmTimeArr[0];
    $second = substr("0".$second,-2,2);
    return "$year-$month-$mday $hour:$minute:$second";
}
