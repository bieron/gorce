var legend = $("#legend");
google.maps.event.addDomListener(window, 'load', function() {
	var mapOptions = {
		 center: new google.maps.LatLng(49.56, 20.14),
		 zoom: 12,
		 mapTypeId: google.maps.MapTypeId.TERRAIN
	  };
	  var map = new google.maps.Map(document.getElementById("map-canvas"),
			mapOptions);

	$.getJSON('ajax/gorce.pl').always(function(data) {
		//console.log(data)

		$.each( data, function( i, item ) {
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng( item.lat, item.lon ),
				map: map,
				title: item.name
			})
			google.maps.event.addDomListener(marker,'click', function() {
				var title = '<h2>' + item.name + '</h2>';
				legend.html(title);
				$.getJSON('ajax/gorce.pl?id=' + item.id).always(function(data) {
					var html = '<ul>'
					for(var i in data)
						html += '<li><img src="photos/' + data[i] + '.jpg"></li>'
					legend.html(title + html)
				})
			})
		})
	
	})
})
