#!/usr/bin/perl -sw
use lib '/home/eaiibgrp/jbieron/perl_modules/lib';
use DBI;
use CGI;

my$q = new CGI;
my%heads = map { $_ => $q->http($_) } $q->http();
unless($heads{HTTP_X_REQUESTED_WITH}) {
  	print $q->redirect('http://student.agh.edu.pl/~jbieron/gorce.dev');
}
my$dbh = DBI->connect('DBI:SQLite:../aux/gorce-dev.db');

print $q->header('application/json');
$rsp = '[';
if ($ENV{QUERY_STRING}) {
	die unless $ENV{QUERY_STRING} =~ /id=\d+/;
	my$id = substr($ENV{QUERY_STRING}, 3);
	my$sth = $dbh->prepare('SELECT url FROM photo WHERE hut=' . $id);
	$sth->execute();

	while(my$ref = $sth->fetchrow_hashref()) {
		$rsp .= "\"$ref->{url}\",";
	}
} else {
	my$sth = $dbh->prepare('SELECT id,name,lat,lon,when_t,state FROM hut');
	$sth->execute();
	
	while(my$ref = $sth->fetchrow_hashref()) {
		$rsp .= "{\"id\": $ref->{id}, \"name\": \"$ref->{name}\","
				. "\"lat\": $ref->{lat}, \"lon\": $ref->{lon},"
				. "\"when_t\": \"$ref->{when_t}\","
				. "\"state\": $ref->{state}},";
	}
}
$rsp = substr($rsp, 0, -1) unless ( length($rsp)==1 );#because if no data, replaces '[' for ']'
print $rsp . ']';
