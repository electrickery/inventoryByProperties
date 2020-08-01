#!/usr/bin/perl
#
use strict;
use warnings;

our $numFile = "theNumber.txt";

#my $descFile = "../dataVanJaak/boards.csv";
#my $descFile = "../dataVanJaak/ORG_IBMpc.csv";
#my $descFile = "../dataVanJaak/portables.csv";
my $descFile = "../dataVanJaak/ideHarddisks.csv";
#my $location = "JaakSite/boards/";
#my $location = "JaakSite/IBM/";
#my $location = "JaakSite/portables/";
my $location = "JaakSite/ideHarddisks/";


unless (-r $descFile && -e $descFile) { die "$0: $descFile not found. aborting."; }

open IFH, "<$descFile"  or die "$0: error opening \'$descFile\'";

my $line;
my $lineCount = 0;
my @propNames;
my @propValues;
my %props;

while ($line = <IFH>) {
    if ($lineCount == 0) {
        @propNames = &processNames($line);
    } else {
        @propValues = &processValues($line);
        my $propCount = @propNames;
        print " propCount = $propCount\n";
        for (my $i = 0; $i < $propCount; $i++) {
            if ($propNames[$i] eq "id") {
                $props{"id"} = &getNextNumber();
            } else {
                if (defined($propValues[$i]) && $propValues[$i] ne "") {
                    my $name = &sanitizeString($propNames[$i]);
                    unless ($name =~ m/^\s*$/) {
                        $props{$name} = $propValues[$i];
                    }
                }
            }
        }
        my $fileName = $location . &sanitizeString(&createFileName(%props));
        print "fileName: $fileName\n";
        open OFH, ">$fileName"  or die "$0: error opening \'$fileName\'";
        foreach my $key (keys %props) { print OFH "$key = $props{$key}\n"; }
        close OFH;
    }
    print "\n";
    $lineCount++;
}

sub processNames() {
    my ($line) = @_;
    my @names;
    chomp $line;
#    $line ~= 
    print "n: " . $line . "\n";
    (@names) = split(";", $line);
    return @names;
}

sub processValues() {
    my ($line) = @_;
    my @props;
    chomp $line;
    print "   " . $line . "\n";
    (@props) = split(";", $line);
    return @props;
}

sub createFileName($$) {
    (%props) = @_;
    my $name = $props{'fabrikant'} . "_" . $props{'model'} . "_" . $props{'id'} . ".properties";
    $name =~ s/\s+/_/g;
    return $name;
}

sub getNextNumber() {
    unless (-r $numFile && -e $numFile) { die "$0: PANIC: $numFile not found. aborting."; }
    open my $ifh, '<', $numFile or die "Can't open file $!";
    my $file_content = do { local $/; <$ifh> };
    close $ifh;

    chomp $file_content;
#    print $file_content . "\n";
    my $number = hex($file_content);
    $number++;
    $file_content = sprintf("%06X", $number);
#    print $file_content . "\n";

    unlink $numFile;
    open my $ofh, '>', $numFile or die "Can't open file $!";
    print $ofh $file_content . "\n";
    close $ofh;

    return $file_content
}

sub sanitizeString() {
    my ($name) = @_;
    $name =~ s/\s+/-/g;
    $name =~ s/[\|\/:;=\$\!\@\#%\^\&\*\(\)\[\]]/_/g;
    return $name;
}
