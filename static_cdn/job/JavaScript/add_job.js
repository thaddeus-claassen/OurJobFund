$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        if ($('#id_latitude').val() == 0 || $('#id_longitude').val() == 0) {
            var loc = $('#location').val();
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
            var pi = 3.14159265;
            $('#id_latitude').val(center.lat() * (pi / 180));
            $('#id_longitude').val(center.lng() * (pi / 180));
            $('#create-job-form').submit();
        } else {
            $('#location-validation').text("Invalid Location.");
            $('#location-validation').css('color', 'red');
        }// end if-else
    });
}// end applyLocation()