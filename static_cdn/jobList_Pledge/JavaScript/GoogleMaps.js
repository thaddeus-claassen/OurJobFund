$('document').ready(function() {
    // function init_map(){var myOptions =
    //                     {zoom:10,center:new google.maps.LatLng(51.48683214093292,0.7415349128906401),
    //                         mapTypeId: google.maps.MapTypeId.ROADMAP};
    //                         map = new google.maps.Map(document.getElementById('gmap_canvas'), myOptions);
    //                         marker = new google.maps.Marker({map: map,position:
    //                                 new google.maps.LatLng(51.48683214093292,0.7415349128906401)});
    //                         infowindow = new google.maps.InfoWindow({content:'<strong>Title</strong><br><br>'});
    //                     google.maps.event.addListener(marker, 'click', function(){infowindow.open(map,marker);});
    //                     infowindow.open(map,marker);
    //                 }google.maps.event.addDomListener(window, 'load', init_map);

    $(function() {
                            var mapOptions = {
                                zoom: 8,
                                center: new google.maps.LatLng(-34.397, 150.644)
                            };
                            var map = new google.maps.Map($("#map-canvas")[0], mapOptions);
                            // listen for the window resize event & trigger Google Maps to update too
                            $(window).resize(function() {
                                // (the 'map' here is the result of the created 'var map = ...' above)
                                google.maps.event.trigger(map, "resize");
                            });
                        });
});



