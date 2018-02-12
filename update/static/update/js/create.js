
var canSubmit = true;

$(document).ready(function() {
    changeOptionsIfTypeisFinish();
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
            $('#error_message').text(format);
        }// end if-else
    });
});

function changeOptionsIfTypeisFinish() {
    var type = $('#submit_button').attr('name').split('_')[1];
    if (type === 'finish') {
        $('option[value=work]').remove();
        $('#id_money_request-wrapper').css('display', 'none');
    }// end if
}// end changeOptionsIfTypeisFinish()

function changedType() {
    if ($('#id_type').find(':selected').val() == 'work') {
        $('#id_money_request-wrapper').css('display', 'inline');
    } else {
        $('#id_money_request-wrapper').css('display', 'none');
    }// end if-else
}// end changedType()

function correctFormat(type) {
    var errorMessage = "";
    if (type === 'pledge' || type === 'work') {
        var amount;
        if (type === 'pledge') amount = parseFloat($('#id_pledge').val());
        else amount = parseFloat($('#id_money_request').val());
        var isFloat = !isNaN(amount);
        if (isFloat) {
            if (amount != amount.toFixed(2)) {
                errorMessage = "Must have at most two decimal places";
            }// end if
        } else {
            errorMessage = "Not a valid number";
        }// end if-else
    } // end if
    return errorMessage;
}// end pledgeErrorMessage()