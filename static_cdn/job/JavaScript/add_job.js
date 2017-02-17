$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        var loc = $('#location').val();
        if (loc.length > 0) {
            applyLocation(loc);                
            event.preventDefault();
        }// end if
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
            $('#name').val($('#id_name').val());
            $('#latitude').val(latitude);
            $('#longitude').val(longitude);
            $('#tags').val($('#id_tags').val());
            $('#description').val($('#id_description').val());
            $('#create-job-form-two').submit();
        } else {
            $('#location-validation').text("Invalid Location.");
            $('#location-validation').css('color', 'red');
        }// end if-else
    });
}// end applyLocation()