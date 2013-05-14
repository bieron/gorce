#!/usr/bin/perl -sw
use lib '/home/eaiibgrp/jbieron/perl_modules/lib';
use CGI;

sub include {
	open my$fh, '<', shift;
	while(<$fh>) {chomp; print}
	close $fh;
}

my$qry = new CGI;
my$cookie = $qry->cookie('welcome');
if($cookie) {
	print $qry->header(-charset => 'utf-8');
	include 'html/head.html';
	include 'html/welcome.html';
} else {
	my$label = 'Powiedz przyjacielu i wejdź';
	my$pass = $qry->param('pass');
	open $read, '<', 'aux/phrase';
	my$phrase = <$read>;
	close $read;
	chomp $phrase;
	if($pass eq $phrase) {
		$cookie = $qry->cookie(
			-name=>'welcome',
			-value=>'home',
			-expires=>'0',
#			-path=>'/~jbieron/gorce.dev'
			-path=>'/'
		);
		print $qry->header(
			-cookie => $cookie, 
			-charset=>'utf-8', 
			-Location => $qry->url() 
		);
	} elsif(lc $pass eq 'mellon') {
		$label = '...srsly?';
	} 
	print $qry->header(-charset => 'utf-8');
	include 'html/head.html';
	open my$read, '<', 'html/form.html';
	while(<$read>) { 
		chomp;
		if($_ eq '=') {print $label}
		else {print}
	}
	close $read;
}
