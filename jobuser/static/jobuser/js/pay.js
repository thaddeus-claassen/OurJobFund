var canSubmit = true;

$(document).ready(function() {
    $('form').submit(function(e) {
        var format = correctFormat();
        if (format === "") {
            if (canSubmit) {
                canSubmit = false; 
            } else {
                e.preventDefault();
            }// end if-else
        } else {
            $('#amount-error-message').remove();
            $('#id_amount').after("&nbsp;&nbsp;&nbsp;<span id='amount-error-message'>" + format + "</span>");
            e.preventDefault();
        }// end if-else
    });
});

function correctFormat() {
    var errorMessage = "";
    var amount = parseFloat($('#id_amount').val());
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