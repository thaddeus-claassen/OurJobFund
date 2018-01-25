var canSubmit = true;

$(document).ready(function() {
    toggleType();
    $('#id_type').change(function () {
        toggleType();
    });
    $('#id_amount').after('<span id="amount_error"></span>');
    $('#post_update_form').submit(function(e) {
        format = correctFormat();
        if (format === "") {
            if (canSubmit) {
                canSubmit = false;
            } else {
                e.preventDefault();
            }// end if-else
        } else {
            $('#id_amount').after(format);
            }// end if-else  
        }// end if-else
    });
});

function toggleType() {
    var type = $('#id_type').val();
    if (type === 'Comment') {
        $('#id_title-wrapper').css('display', 'inline');
        $('#id_title').val('');
        $('#id_amount-wrapper').css('display', 'none');
        $('#id_amount').val(10);
        $('#id_pay_to-wrapper').css('display', 'none');
        $('#id_pay_to').val('@@@');
        $('#id_images-wrapper').css('display', 'inline');
    } else if (type === 'Working') {
        $('#id_title-wrapper').css('display', 'none');
        $('#id_title').val(type);
        $('#id_amount-wrapper').css('display', 'none');
        $('#id_amount').val(10);
        $('#id_pay_to-wrapper').css('display', 'none');
        $('#id_pay_to').val('@@@');
        $('#id_images-wrapper').css('display', 'none');
    } else if (type === 'Finished') {
        $('#id_title-wrapper').css('display', 'none');
        $('#id_title').val(type);
        $('#id_amount-wrapper').css('display', 'none');
        $('#id_amount').val(10);
        $('#id_pay_to-wrapper').css('display', 'none');
        $('#id_pay_to').val('@@@');
        $('#id_images-wrapper').css('display', 'none');
    } else if (type === 'Pledge') {
        $('#id_title-wrapper').css('display', 'none');
        $('#id_title').val(type);
        $('#id_amount-wrapper').css('display', 'inline');
        $('#id_amount').val('');
        $('#id_pay_to-wrapper').css('display', 'none');
        $('#id_pay_to').val('@@@');
        $('#id_images-wrapper').css('display', 'none');
    } else if (type === 'Pay') {
        $('#id_title-wrapper').css('display', 'none');
        $('#id_title').val(type);
        $('#id_amount-wrapper').css('display', 'inline');
        $('#id_amount').val('');
        $('#id_pay_to-wrapper').css('display', 'inline');
        $('#id_pay_to').val('');
        $('#id_images-wrapper').css('display', 'none');
    }// end if
}// end toggleType()

function correctFormat() {
    var errorMessage = "";
    var amount = parseFloat($('#id_amount').val());
    var isFloat = !isNaN(amount);
    if (isFloat) {
        if (amount != amount.toFixed(2)) {
            errorMessage = "Must have at most two decimal places";
        }// end if
    } else {
        errorMessage = "Not a valid number";
    }// end if-else
    return errorMessage;
}// end pledgeErrorMessage()