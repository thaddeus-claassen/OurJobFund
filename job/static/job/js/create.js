var canSubmit = true;

$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        var format = correctFormat();
        if (format === "") {
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
        } else {
            $('#amount-error-message').remove();
            $('#id_amount').after("&nbsp;&nbsp;&nbsp;<span id='amount-error-message'>" + format + "</span>");
            e.preventDefault();
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
            $('#id_location').after("<span id='location-error'>Could not verify location.</span>");
            $('#location-error').css('color', 'red');
            can 
        }// end if-else
    });
}// end applyLocation()

function correctFormat() {
    var errorMessage = "";
    var amount = parseFloat($('#id_pledge').val());
    if (amount === "") {
        amount = 0;
    } else {
        var isFloat = !isNaN(amount);
        if (isFloat) {
            if (amount != amount.toFixed(2)) {
                errorMessage = "Cannot have more than two decimal places.";
            }// end if
        } else {
            errorMessage = "Not a valid number";
        }// end if-else
    }// end if-else
    return errorMessage;
}// end pledgeErrorMessage()