function toLL( i, l ) { 
	i = (i*1000000).toFixed()/1000000 
	z = 0;
	if(i < 0) 
		i *= -1, ++z;
	return i+=l[z]
}
function changeOverview( html ) {
	overview.animate({opacity:0},{duration:250, complete:function() {
		overview.html(html); overview.animate({opacity:1},250) }
	})
}
function resize() {resizing.height( window.innerHeight - 62)}
function feedLL(pos, flag) {
	if(flag) latLng.addClass('important')
	else	 latLng.removeClass('important')
	latLng.html( toLL( pos.lat(), 'NS' ) + ', ' + toLL( pos.lng(), 'EW' ) )
}
var startLL = new google.maps.LatLng(49.56, 20.14)
var overview = $("#overview")
var latLng = $("#latLng")
var resizing = $('.wrapper,.overview-box')
var m
google.maps.event.addDomListener(window, 'load', function() {
	resize()
	window.onresize = resize
	var mapOptions = {
		 center: startLL,
		 zoom: 12,
		 mapTypeId: google.maps.MapTypeId.TERRAIN
	};
	var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions)

	google.maps.event.addListener(map, 'mousemove', function(ev) { feedLL(ev.latLng,0) })
	var legendary = {'hut': [], 'ambo': [], 'other': [], 'shelter': [], 'Bene': []}
	var cache = {}
	var first = true
	$.getJSON('ajax/gorce.cgi').always(function(data) {
		$.each( data, function( i, item ) {
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng( item.lat, item.lon ),
				map: map,
				title: item.name,
				animation: google.maps.Animation.DROP,
			})
//			m = marker
			switch(item.state) {
			case 1: case 2: case 3: case 4: case 5: case 6:
				legendary.hut.push( marker ); 
				marker.setIcon('https://maps.gstatic.com/mapfiles/ms2/micons/campground.png')
				break
			case 7: case 8:
				legendary.ambo.push( marker ); break
			case 11:
				legendary.Bene.push( marker ); break
			case 12:
				legendary.shelter.push( marker ); break
			default:
				legendary.other.push( marker )
			}
			
			google.maps.event.addDomListener(marker,'click', function() {
				if(first) {
					first = false
					$('.map-box').animate({marginRight:'340px'},500)
					$('.overview-box').animate({width:'340px'},500)
				}
				$('.overview-box').mouseover(function() {feedLL(marker.position, 1)})
				if(typeof(cache[item.id])!='undefined') {
					changeOverview( cache[item.id] )
					return;
				}
				$.getJSON('ajax/gorce.cgi?id=' + item.id).success(function(data) {
					var html = '<h2>' + item.name + '</h2><ul>'
					for(var i in data)
						html += '<li><img alt="'+ item.name +'" src="photos/' + data[i] + '.jpg"></li>'
					html += '</ul>'
					cache[item.id] = html
					changeOverview(html)
				})
			})
			google.maps.event.addListener(marker, 'mouseover', function(ev) {
				feedLL(marker.position, 1)
			})
		})
		$.each({'#hutBtn': 'hut', '#amboBtn':'ambo', '#BeneBtn': 'Bene', '#shelterBtn': 'shelter', '#otherBtn': 'other'}, function(i,el) {
			$(i).click(function() {
			$(this).toggleClass('pressed')
			if(legendary[el].length==0) return
			var desired = !legendary[el][0].visible
			for(var m in legendary[el])
				legendary[el][m].setVisible( desired )
			})
		})
	})//end json get markers
	$('#resetBtn').click(function(){ map.panTo(startLL); map.setZoom(12); return false})
	//set entry state
	google.maps.event.addListenerOnce(map, 'idle', function(){
		$('#BeneBtn,#shelterBtn').click()
	})
})
