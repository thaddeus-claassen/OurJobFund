var canSubmit = true;
var stripeSubmitted = false;
var handler;

$(document).ready(function() {
    $('#form').submit(function(e) {
        if ($('#id_pay_through').val() === 'Stripe') {
            if (stripeSubmitted) {
                if (canSubmit) {
                    canSubmit = false;
                } else {
                    e.preventDefault();
                }// end if-else
            } else {
                stripeSubmitted = true;
                handler.open({
                    amount: $('#id_amount').val() * 100,
                    description: "Payment to " + $('#id_receiver').val(), 
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
    });
    handler = StripeCheckout.configure({
        key: 'pk_test_DF7zGC0IPpcOQyWr2nWHVLZ6',
        token: function(token) {
            $('#stripe_token').val(token.id);
            $('#form').submit();
        },
    });
    $(window).on('popstate', function() {
        handler.close();
    });
});
