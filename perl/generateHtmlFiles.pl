#!/usr/bin/perl
use strict;
use warnings;
use Config::Properties;
use File::Basename;
use Path::Iterator::Rule;

our $SITEURL = "http://jaaks.be/inventaris/";
our $PROPEXT = ".properties";
our $PROPFILEPATT = "_([0-9A-F]{6})${PROPEXT}\$";
our $COMMENTEXT = ".txt";
our $COMMENTPATT = "_([0-9A-F]{6})${COMMENTEXT}\$";

my @dirs = @ARGV;
if (@dirs == 0) { push(@dirs, "site") };
our $refDir = "site/ref/";
my $objectUrlBase = $SITEURL;

my @objectFiles = &getObjMetaDataFiles(@dirs);
print "objectCount: " . @objectFiles . "\n";

foreach my $of (@objectFiles) {
#    print "  > " . $of . "\n";
    my $props = Config::Properties->new(file => $of, order => 'keep');
    my $title = $props->getProperty('fabrikant') . " " . $props->getProperty('model', "") . " " . $props->getProperty('naam', "");
    $title =~ s/^\s+|\s+$//g;          # trim whitespace
    $of =~ m/$PROPFILEPATT/i; # filter identifier
    my $id = $1;
    print("'" . $title . "'  " . $id . "\n");
    &generateRefPage($refDir, $props, $objectUrlBase, $of);
    &generateObjectPage($of, $props);
}

sub generateRefPage() {
    my ($refDir, $props, $urlBase, $objectTextFile) = @_;
    my $objectHtmlFile = &createHtmlFileName($objectTextFile);
    my $refFileName = $refDir . basename($objectHtmlFile);
    open my $rfh, '>', $refFileName or die "Can't open file '" . $refFileName . "' $!";
    my $file_content = &getRefHtmlTemplate();
    $file_content =~ s/%%OBJECTURL%%/${urlBase}${objectHtmlFile}/g;
    print $rfh $file_content . "\n";
    close $rfh;
}

sub generateObjectPage() {
    my ($objectTextFile, $props) = @_;
    my $objectHtmlFile = &createHtmlFileName($objectTextFile);
    my $title = $props->getProperty('fabrikant') . " " . $props->getProperty('model', "") . " " . $props->getProperty('naam', "");
    $title =~ s/^\s+|\s+$//g; # trim whitespace
    open my $hfh, '>', $objectHtmlFile or die "Can't open file '" . $objectHtmlFile . "' $!";
    my $file_content = &getObjectHtmlTemplate();
    $file_content =~ s/%%TITLE%%/$title/;
    $file_content =~ s/%%NAME%%/$title/;
    my $metadataTable = &generateMetadataTableTemplate($props);
    $file_content =~ s/%%METADATA%%/$metadataTable/;
    my $dir = dirname($objectTextFile);
    $objectTextFile =~ m/$PROPFILEPATT/; # filter identifier
    my $id = $1;
    my @types = ['jpg', 'png', 'gif'];
    my $imageSection = &getObjImageSection($dir, $id, ".", @types);
    $file_content =~ s/%%IMAGES%%/$imageSection/;
    my $commentSection = &getObjCommentSection($dir, $id);
    $file_content =~ s/%%COMMENTS%%/$commentSection/;
    my $genDate = &getCurrentTime();
    $file_content =~ s/%%DATE%%/$genDate/;
    print $hfh $file_content;
    close $hfh;
}

sub generateMetadataTableTemplate() {
    my ($props) = @_;
    my $table_content = &getMetadataTableTemplate();
    my $tableRowSet = "";
    my @propKeys = $props->propertyNames();
    foreach(@propKeys) {
        my $key = $_;
        my $value = $props->getProperty($key);
        my $tableRow = &getMetadataRowTemplate();
        $tableRow =~ s/%%KEY%%/$key/;
        if ($value =~ m|http[s]://|) {
            my $linkValue = "<a href='${value}'>${value}</a>";
            $tableRow =~ s/%%VALUE%%/$linkValue/;
        } else {
            $tableRow =~ s/%%VALUE%%/$value/;
        }
        $tableRowSet = $tableRowSet . $tableRow;
    }
#    print $tableRowSet;
    $table_content =~ s/%%METADATAROWSET%%/$tableRowSet/;
    return $table_content;
}

sub createHtmlFileName() {
    my ($objectTextFile) = @_;
    my($filename, $dirs, $suffix) =  fileparse($objectTextFile, qr/\.[^.]*/);
    my $objectHtmlFile = $dirs . "/" . $filename . ".html";
    $objectHtmlFile =~ s/$PROPEXT$/.html/i; # replace any-case txt-extension with html
    $objectHtmlFile =~ s|^\./||; # remove prefixed './'
    return $objectHtmlFile;
}

sub getObjMetaDataFiles($$) {
    my (@dirs) = @_;
    my $rule = Path::Iterator::Rule->new;
#    $rule->skip_subdirs(qr/$refDir/)->file;
    my @files;
    for my $fileName ( $rule->all( @dirs ) ) {
        if ($fileName =~ m/^$refDir/) { next; }
#        print "m $fileName m/$PROPFILEPATT/i \n";
        if ($fileName =~ m/$PROPFILEPATT/i) { # filter files ending with _XXXXXX.properties
#            print " $fileName      <<<<<<< \n";
            push (@files, $fileName);
#        } else {
#            print "\n";
        }
    }
    return @files;
}

sub getObjImageSection() {
    my ($dir, $id) = @_;
    my @files = &getObjImageFiles($dir, $id);
    my $imageSection = "";
    foreach (@files) {
        my $file = $_;
        my $imageParagraph = &getImagesTemplate();
        my $imageUrl = $file;
        $imageParagraph =~ s/%%IMAGE%%/$imageUrl/;
        $imageSection = $imageSection . $imageParagraph;
    }
    return $imageSection;
}

sub getObjImageFiles($$) {
    my ($dir, $id) = @_;
    my @files;
    my $rule = Path::Iterator::Rule->new(order => 'keep');
    $rule->iname("*.jpg", "*.png", "*.gif");
    my $idPattern = "_$id.";
    for my $fileName ( $rule->all( $dir ) ) {
        if ($fileName =~ m/$idPattern/i) {
            $fileName = basename($fileName);
            push (@files, $fileName);
        }
    }
    return @files;
}

sub getObjCommentSection() {
    my ($dir, $id) = @_;
    my @files = &getObjCommentFiles($dir, $id);
    my $commentSection = "";
        if (@files > 0) {
            $commentSection = $commentSection . getCommentsHeader();
        }
    foreach (@files) {
        my $file = $_;
        open my $cfh, '<', $file or die "Can't open file '" . $file . "' $!";
        chomp(my @lines = <$cfh>);
        close $cfh;
        foreach (@lines) {
            my $line = $_;
            if ($line ne "") {
                my $commentParagraph = &getCommentTemplate();
                $commentParagraph =~ s/%%COMMENT%%/$line/;
                $commentSection = $commentSection . $commentParagraph;
            }
        }
    }
    return $commentSection;
}

sub getObjCommentFiles($$) {
    my ($dir, $id) = @_;
    my @files;
    my $rule = Path::Iterator::Rule->new(order => 'keep');
    $rule->iname("*" . $COMMENTEXT);
    my $idPattern = "_" . $id . ".";
    for my $fileName ( $rule->all( $dir ) ) {
        if ($fileName =~ m/$idPattern/i) {
            push (@files, $fileName);
        }
    }
    return @files;
}

sub getRefHtmlTemplate() {
    return "<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
<html>
    <head>
        <meta http-equiv='Refresh' content=\"0; url='%%OBJECTURL%%'\" />
    </head>
    <body>
        <p>Redirecting to %%OBJECTURL%%</p>
    </body>
</html>
";
}

sub getObjectHtmlTemplate() {
    return "<!doctype html public '-//w3c//dtd html 3.2 fINAL//en'> 
<html>
    <head>
       <title>%%TITLE%%</title>
       <link rel='stylesheet' type='text/css' href='./table.css'>
    </head>
    <body>
        <h2>%%NAME%%</h2>
        %%METADATA%%
        %%IMAGES%%
        %%COMMENTS%%

    <p><i>Latest update: %%DATE%%</i></p>

    </body>
</html>
";
}

sub getMetadataTableTemplate {
    return "<p><table>
%%METADATAROWSET%%
</table></p>
";
}

sub getMetadataRowTemplate { 
    return "<tr><td>%%KEY%%</td> <td>%%VALUE%%</td></tr>
";
}

sub getImagesTemplate {
    return "<p><img src='%%IMAGE%%'/></p>
";
}

sub getCommentTemplate {
    return "<p>%%COMMENT%%</p>
";
}

sub getCommentsHeader() {
    return "<h3>Comments</h3>";
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
