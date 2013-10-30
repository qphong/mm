var map;
var pointArr;
var segArr;

function initialize() {
	var myOptions = {
		center: new google.maps.LatLng(1.364922, 103.819427),
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
    map = new
		google.maps.Map(document.getElementById("map_canvas"),
			myOptions);
}

var iter = 0;
var markers = [];
var arrows = [];
function addRoute() {

	if (iter < points.length) {
		var marker = new google.maps.Marker({
				position:points[iter],
				map:map,
				title:pointsInfo[iter]
		});
		markers.push(markers);
	}

	if (iter < segs.length) {
		var path = new google.maps.Polyline({
				path:segs[iter],
				strokeColor: "#FF0000",
				strokeOpacity:1.0,
				strokeWeight:2,
				map:map
		});
		var arrow = createArrowOverlay(map, segs[iter][0], segs[iter][1], "#000000", 1.0, ids[iter]);
		arrows.push(arrow);
	}

	iter++;
}


function addAllPoints() {

	for (var i = 0; i < points.length; i++) {
		var marker = new google.maps.Marker({
			position:points[i],
			map:map,
			title:pointsInfo[i]
		});
	}
	
}


function addAllSegments() {
	
	for (var i = 0; i < segs.length; i++) {
		var path = new google.maps.Polyline({
			path:segs[i],
			strokeColor: "#FF0000",
			strokeOpacity:1.0,
			strokeHeight:2,
			map:map
		});
		var arrow = createArrowOverlay(map, segs[i][0], segs[i][1], "#000000", 1.0, ids[i]);
		arrows.push(arrow);
	}
	
}


// function removeAllMarkers() {
// 	for (var i = 0; i < markers.length; i++) {
// 		markers[i].setMap(null);
// 	}
// }


// function removeMarker(refLatLng) {
// 	for (var i = 0; i < markers.length; i++) {
// 		//var curLatLng = markers[i].getPosition();
// 		//if (refLatLng.lat() == curLatLng.lat() && refLatLng.lng() == curLatLng.lng())
// 			markers[i].setMap(null);
// 	}
// }

// function removeArrow(startLatLng, endLatLng) {
// 	for (var i = 0; i < arrows.length; i++) {
// 		arrows[i].setMap(null);
// 	}
// }