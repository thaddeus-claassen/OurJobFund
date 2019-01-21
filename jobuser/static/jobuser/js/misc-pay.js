function correctFormat() {
    var errorMessage = "";
    var amount = $('#id_amount').val();
    if (amount === "") {
        amount = 0;
    } else {
        amount = parseFloat(amount);
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

function errorMessage() {
    $('#amount-error-message').remove();
    $('#id_amount').after("&nbsp;&nbsp;&nbsp;<span id='amount-error-message'>" + format + "</span>");
}// end errorMessage()