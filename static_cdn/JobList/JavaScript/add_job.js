$('document').ready(function() {
    // CKEDITOR.replace( 'editor1' );
    $('label:text').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
        }// end if
    });
//    $('label:textarea').keydown(function(event) {
//        if (event.which == 13) {
//            event.preventDefault();
//        }// end if
//    });
    $('#location').on('input', function(event) {
        var address = $('#location').val();
        applyLocation(address);
    });
});

function applyLocation(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var center = results[0].geometry.location;
            var pi = 3.14159265;
            var latitude = center.lat() * (pi / 180);
            var longitude = center.lng() * (pi / 180);
            $('#latitude').val(latitude);
            $('#longitude').val(longitude);
        } else {
            $('#location-validation').delay(2000).val("Location not valid.");
        }// end if-else
    });
}// end applyLocation()