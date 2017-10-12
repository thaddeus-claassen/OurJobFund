$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        if ($('#id_latitude').val() == 0 || $('#id_longitude').val() == 0) {
            var loc = $('#id_location').val();
            if (loc.length > 0) {
                event.preventDefault();
                applyLocation(loc);
            }// end if
        }// end if
    });
});

function applyLocation(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var center = results[0].geometry.location;
            $('#id_latitude').val(center.lat());
            $('#id_longitude').val(center.lng());
            $('#create-job-form').submit();
        } else {
            $('#id_location').after("<span>Google Maps could not verify your location.</span>");
            $('#location-validation').css('color', 'red');
        }// end if-else
    });
}// end applyLocation()