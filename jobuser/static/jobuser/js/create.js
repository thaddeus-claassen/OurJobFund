var canSubmit = true;

$(document).ready(function() {
    $('#id_type').change(function() {
        changedType();
    });
    $('#form').submit(function(e) {
        var type = $('#submit_button').attr('name').split('_')[1];
        format = correctFormat(type);
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

function changedType() {
    if ($('#id_type').find(':selected').val() === 'Working') {
        $('#id_amount-wrapper').css('display', 'inline');
    } else {
        $('#id_amount-wrapper').css('display', 'none');
    }// end if-else
}// end changedType()

function correctFormat(type) {
    var errorMessage = "";
    if (type === 'pledge' || type === 'work') {
        var amount = parseFloat($('#id_amount').val());
        var isFloat = !isNaN(amount);
        if (isFloat) {
            if (amount != amount.toFixed(2)) {
                errorMessage = "Must have at most two decimal places";
            } else if (type === 'pay' && $('#type').val() === 'Credit' && amount < 0.5) {
                errorMessage = "You cannot pay less than $0.50 with card."
            }// end if
        } else {
            errorMessage = "Not a valid number";
        }// end if-else
    } // end if
    return errorMessage;
}// end pledgeErrorMessage()