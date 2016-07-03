/**
 * Created by Hp on 12/16/2015.
 */

var service,
    marker = null,
    map,
    autocomplete_search,
    autocomplete_source,
    autocomplete_dest,
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

    geolocate();
}

function initialize() {

    var mapOptions = {
        mapTypeControl: false,
        center: new google.maps.LatLng(31.555128, 74.358038),
        zoom: 12
    };
    map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    autocomplete_search = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('search_origin')),
        {types: ['geocode']});

    autocomplete_search.setComponentRestrictions({'country': 'PK'});
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.

    google.maps.event.addListener(autocomplete_search, 'place_changed', function () {
        fillPlaceSearch();
    });

    //directions

    autocomplete_source = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('source')),
        {types: ['geocode']});

    autocomplete_source.setComponentRestrictions({'country': 'PK'});
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    google.maps.event.addListener(autocomplete_source, 'place_changed', function () {
        fillPlaceSrc();
    });

    autocomplete_dest = new google.maps.places.Autocomplete(
        /** @type {HTMLInputElement} */(document.getElementById('destination')),
        {types: ['geocode']});
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    autocomplete_dest.setComponentRestrictions({'country': 'PK'});
    google.maps.event.addListener(autocomplete_dest, 'place_changed', function () {
        fillPlaceDest();
    });

    ////////////

    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
}

var search_place = null;

function fillPlaceSearch() {
    directionsDisplay.setMap(null);
    var place = autocomplete_search.getPlace();
    search_place = place;
    var latitude = place.geometry.location.lat();
    var longitude = place.geometry.location.lng();
    document.getElementById('search').value = latitude.toString() + ',' + longitude.toString();
    moveToLocation(latitude, longitude);
    create_marker(latitude, longitude);
}


function geolocate() {

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
    map.setZoom(12);
}

var dest_place = null;
var src_place = null;

function calcRoute() {
    directionsDisplay.setMap(map);
    if (src_place && dest_place) {
        var coords_src = new google.maps.LatLng(src_place.geometry.location.lat(), src_place.geometry.location.lng());
        var coords_dest = new google.maps.LatLng(dest_place.geometry.location.lat(), dest_place.geometry.location.lng());

        var request = {
            origin: coords_src,
            destination: coords_dest,
            travelMode: google.maps.TravelMode.DRIVING
        };
        directionsService.route(request, function (result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                marker_dest.setMap(null);
                marker_src.setMap(null);
                directionsDisplay.setDirections(result);
            }
        });
    }
}


function fillPlaceSrc() {
    directionsDisplay.setMap(null);
    var place = autocomplete_source.getPlace();
    src_place = place;
    marker_src = new google.maps.Marker({
        position: place.geometry.location,
        map: map,
        title: "Source!"
    });
    var infowindow = new google.maps.InfoWindow();
    marker_src.setMap(map);
    google.maps.event.addListener(marker_src, 'click', function () {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
    var latitude = place.geometry.location.lat();
    var longitude = place.geometry.location.lng();
    document.getElementById('src_val').value = latitude.toString() + ',' + longitude.toString();
    moveToLocation(latitude, longitude);
    calcRoute();
}

var marker_src = null;
var marker_dest = null;

function fillPlaceDest() {
    directionsDisplay.setMap(null);
    var place = autocomplete_dest.getPlace();
    dest_place = place;
    marker_dest = new google.maps.Marker({
        position: place.geometry.location,
        map: map,
        title: "Destination!"
    });
    var infowindow = new google.maps.InfoWindow();
    marker_dest.setMap(map);
    google.maps.event.addListener(marker_dest, 'click', function () {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
    var latitude = place.geometry.location.lat();
    var longitude = place.geometry.location.lng();
    document.getElementById('dest_val').value = latitude.toString() + ',' + longitude.toString();

    moveToLocation(latitude, longitude);
    calcRoute();
}