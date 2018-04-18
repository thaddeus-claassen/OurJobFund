var canSubmit = true;

$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        if (canSubmit) {
            canSubmit = false;
            if ($('#id_latitude').val() === "" || $('#id_longitude').val() === "") {
                var loc = $('#id_location').val();
                if (loc.length > 0) {
                    event.preventDefault();
                    applyLocation(loc);
                }// end if
            }// end if
        } else {
            event.preventDefault();
        }// end if-else
    });
});

function applyLocation(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address}, function(results, status) {
        canSubmit = true;
        if (status == google.maps.GeocoderStatus.OK) {
            var center = results[0].geometry.location;
            $('#id_latitude').val(center.lat());
            $('#id_longitude').val(center.lng());
            $('#create-job-form').submit();
        } else {
            $('#id_location').after("<span id='location-error'>Must be a valid location on Google Maps</span>");
            $('#location-error').css('color', 'red');
        }// end if-else
    });
}// end applyLocation()
