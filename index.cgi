#!/usr/bin/perl -sw
use lib '/home/eaiibgrp/jbieron/perl_modules/lib';
use CGI;

sub root {
	my$q = shift;
	my$str = $q->url( -absolute => 1 );
	return substr($str, 0, rindex($str, '/'));
}
sub include {
	open my$fh, '<', shift;
	while(<$fh>) {chomp; print}
	close $fh;
}
sub anal {
	my($cookie,$first) = @_;
	open my$anal, '>>', 'anal.txt';
	print $anal $cookie, '|';
	if($first) {
		print $anal 'first';
		#print $anal $cookie->value. '|';
	} else {
		print $anal localtime();
	}
	print $anal '|', $ENV{HTTP_USER_AGENT}, "\n";
	close $anal;
}

my$q = new CGI;
my$cookie = $q->cookie('welcome');

if($cookie) {
	anal( $cookie, 0 );
	print $q->header(-charset => 'utf-8');
	include 'html/head.html';
	include 'html/welcome.html';
#end
} else {
	my$label = 'Powiedz przyjacielu i wejdź';
	my$pass = $q->param('pass') || '';
	open my$read, '<', 'aux/phrase' or die 'Nie mogę sprawdzić hasła';
	my$phrase = <$read>;
	close $read;
	chomp $phrase;
	
	if($pass eq $phrase) {
		#my$time = localtime;
		$cookie = $q->cookie(
			-name=>'welcome',
			-value=> time,
			-expires=>'0',
#			-path=>'/~jbieron/gorce.dev'
#			-path=>'/'
			-path=> root($q)
		);
		anal( $cookie, 1 );

		print $q->header(
			-cookie => $cookie, 
			-charset=>'utf-8', 
			-Location => $q->url() 
		);
#end
	} 
	if(lc $pass eq 'mellon') {
		$label = '...srsly?';
	} 
	print $q->header(-charset => 'utf-8');
	include 'html/head.html';
	open $read, '<', 'html/form.html';
	while(<$read>) { 
		chomp;
		if($_ eq '=') {print $label}
		else {print}
	}
	close $read;
}
