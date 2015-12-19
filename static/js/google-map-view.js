/**
 * Created by Hp on 12/16/2015.
 */

var service,
    marker = null,
    map,
    directionsService = null,
    directionsDisplay;


onload = function () {
    loadScript();
};

function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyAZIMK_aJF9zUVITx7NlyZuIZtAkwj31jA&v=3.exp&' +
        'callback=initialize';
    document.body.appendChild(script);
}

function initialize() {

    var mapOptions = {
        mapTypeControl: false,
        center: new google.maps.LatLng(31.555128, 74.358038),
        zoom: 17
    };
    map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    ////////////

    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
}

function fillPlaceSearch(lon, lat) {

    directionsDisplay.setMap(null);
    moveToLocation(parseFloat(lon), parseFloat(lat));
    create_marker(parseFloat(lon), parseFloat(lat));
}


function moveToLocation(lat, lng) {
    var center = new google.maps.LatLng(lat, lng);
    // using global variable:
    map.panTo(center);
}

function create_marker(lat, lng){
    var myLatlng = {lat: lat, lng: lng};
    if(marker == null)
    {
        marker = new google.maps.Marker({
            position: myLatlng,
            draggable: true,
            map: map,
            title: 'Searched location'
        });
        google.maps.event.addListener(marker, 'dragend', function (evt) {
            document.getElementById('search').innerHTML = evt.latLng.lat().toFixed(8) + ',' + evt.latLng.lng().toFixed(8);
        });
    }
    else {
        marker.position = myLatlng;
    }
}

function calcRoute(lon1, lat1, lon2,lat2) {

    directionsDisplay.setMap(map);

        var coords_src = new google.maps.LatLng(parseFloat(lon1), parseFloat(lat1));
        var coords_dest = new google.maps.LatLng(parseFloat(lon2), parseFloat(lat2));

        var request = {
            origin: coords_src,
            destination: coords_dest,
            travelMode: google.maps.TravelMode.DRIVING
        };
        directionsService.route(request, function (result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(result);
            }
        });

}
