var canSubmit = true;
var stripeSubmitted = false;
var handler;

$(document).ready(function() {
    var handler = StripeCheckout.configure({
        key: 'pk_test_DF7zGC0IPpcOQyWr2nWHVLZ6',
        token: function(token) {
            $('#stripe_token').val(token.id);
            $('form').submit();
        }
    });
    $('form').submit(function(e) {
        var format = correctFormat();
        if (format === "") {
            if ($('#id_pay_through').val() === 'Stripe') {
                if (stripeSubmitted) {
                    //if (canSubmit) {
                    //    canSubmit = false;
                    //} else {
                    //    e.preventDefault();
                    //}// end if-else
                } else {
                    stripeSubmitted = true;
                    handler.open({
                        amount: $('#id_amount').val() * 100,
                        description: "Payment to " + $('#pay_to').val(), 
                    });
                    e.preventDefault();
                }// end if-else
            } else {
                if (canSubmit) {
                    canSubmit = false;
                } else {
                    e.preventDefault();
                }// end if-else
            }// if-else
        } else {
            $('#amount-error-message').remove();
            $('#id_amount').after("&nbsp;&nbsp;&nbsp;<span id='amount-error-message'>" + format + "</span>");
            e.preventDefault();
        }// end if-else
    });
    $(window).on('popstate', function() {
        handler.close();
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