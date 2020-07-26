#!/usr/bin/perl
#
use strict;
use warnings;

print &getNextNumber() . "\n";


sub getNextNumber() {
    my $numFile = "theNumber.txt";

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
