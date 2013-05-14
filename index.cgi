#!/usr/bin/perl -sw
use lib '/home/eaiibgrp/jbieron/perl_modules/lib';
use CGI;

my$qry = new CGI;
my$cookie = $qry->cookie('welcome');
if($cookie) {
	print $qry->header(-charset => 'utf-8');
	open(my$read, '<', 'html/welcome.html');
	while(<$read>) { chomp; print }
	close $read;
} else {
	my$label = 'Powiedz przyjacielu i wejdź';
	my$pass = $qry->param('pass');
	open my$read, '<', 'aux/phrase';
	my$phrase = <$read>;
	close $read;
	chomp $phrase;
	if($pass eq $phrase) {
		$cookie = $qry->cookie(
			-name=>'welcome',
			-value=>'home',
			-expires=>'0',
			-path=>'/~jbieron/gorce.dev'
		);
		print $qry->header(
			-cookie => $cookie, 
			-charset=>'utf-8', 
			-Location => $qry->url() );
	} elsif(lc $pass eq 'mellon') {
		$label = '...srsly?';
	} 
	print $qry->header(-charset => 'utf-8');
	open(my$read, '<', 'html/form.html');
	while(<$read>) { 
		chomp;
		if($_ eq '=') {print $label}
		else {print}
	}
	close $read;
}
