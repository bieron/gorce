#!/usr/bin/perl -sw
use DBI;
my$dbh = DBI->connect('DBI:Pg:dbname=gorce;host=localhost', 'jb','pass',{RaiseError => 1});

print  "Content-type: application/json\n\n";
$rsp = '[';
if ($ENV{QUERY_STRING}) {
	die unless $ENV{QUERY_STRING} =~ /id=\d+/;
	my$id = substr($ENV{QUERY_STRING}, 3);
	my$sth = $dbh->prepare('SELECT url FROM photo WHERE cottage=' . $id);
	$sth->execute();

	while(my$ref = $sth->fetchrow_hashref()) {
		$rsp .= "\"$ref->{url}\",";
	}
} else {
	my$sth = $dbh->prepare('SELECT id,name,lat,lon,when_t FROM cottage');
	$sth->execute();
	
	while(my$ref = $sth->fetchrow_hashref()) {
		$rsp .= "{\"id\": $ref->{id}, \"name\": \"$ref->{name}\","
				. "\"lat\": $ref->{lat}, \"lon\": $ref->{lon},"
				. "\"when_t\": \"$ref->{when_t}\"},";
	}
}
$rsp = substr($rsp, 0, -1) unless ( length($rsp)==1 );#because if no data, replaces '[' for ']'
print $rsp . ']';
