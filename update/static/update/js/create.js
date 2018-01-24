var canSubmit = true;
var firstTimePaySubmitted = true;

$(document).ready(function() {
    toggleType();
    $('#id_type').change(function () {
        toggleType();
    });
    $('#id_amount').after('<span id="amount_error"></span>');
    $('#post_update_form').submit(function(e) {
        if ($('#id_type').val() === 'Pay') {
            if (firstTimePaySubmitted) {
                firstTimePaySubmitted = false;
                $('#amount_error').text('');
                var amount = $('#id_amount').val();
                amount = parseFloat(amount);
                if (isNaN(amount)) {
                    $('#amount_error').text('Please enter a valid amount in USD ($).');
                } else if (amount < 0.5) {
                    $('#amount_error').text('Payment must be at least $0.50.');
                } else {
                    amount = Math.round(amount * 100); // Needs to be an integer!
                    if (Math.floor(amount) === amount) {
                        handler.open({
                            amount: amount,
                        });
                    } else {
                        $('#amount_error').text('Please enter a valid amount in USD ($).');
                    }// end if-else
                }// end if-else
                e.preventDefault();
            }// end if
        } else {
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
    $('#pay_money').click(function() {
        $('#pay_unclicked').css('display', 'none');
        $('#pay_clicked').css('display', 'inline');
    });
    $('#cancel_pay').click(function() {
        $('#pay_clicked').css('display', 'none');
        $('#pay_unclicked').css('display', 'inline');
        $('#pay_for_error').text("");
        $('#pay_amount_error').text("");
    });
    var handler = StripeCheckout.configure({
        key: 'pk_test_DF7zGC0IPpcOQyWr2nWHVLZ6',
        locale: 'auto',
        name: 'OurJobFund',
        description: 'One-time payment to the selected worker',
        token: function(token) {
            $('#stripe_token').val(token.id);
            $('#post_update_form').submit();
        }
    });
    // Close Checkout on page navigation
    $(window).on('popstate', function() {
        handler.close();
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