#!/usr/bin/perl
#
use strict;
use warnings;

#my $descFile = "../dataVanJaak/boards.csv";
#my $descFile = "../dataVanJaak/ORG_IBMpc.csv";
my $descFile = "../dataVanJaak/portables.csv";


unless (-r $descFile && -e $descFile) { die "$0: $descFile not found. aborting."; }

open IFH, "<$descFile"  or die "$0: error opening \'$descFile\'";

my $line;
my $lineCount = 0;
my @propNames;
my @propValues;

while ($line = <IFH>) {
    if ($lineCount == 0) {
        @propNames = &processNames($line);
    } else {
        @propValues = &processValues($line);
        my $propCount = @propNames;
        for (my $i = 0; $i < $propCount; $i++) {
            if (defined $propValues[$i] && $propValues[$i] ne "") {
                print $propNames[$i] . " = " . $propValues[$i] . "\n";
            }
        }
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
