var handler;

$(document).ready(function() {
    handler = StripeCheckout.configure({
        key: 'pk_test_DF7zGC0IPpcOQyWr2nWHVLZ6',
        locale: 'auto',
        name: 'OurJobFund',
        description: 'One-time payment to the selected worker',
        token: function(token) {
            $('#stripe_token').val(token.id);
            $('#form').submit();
        }
    });
    // Close Checkout on page navigation
    $(window).on('popstate', function() {
        handler.close();
    });
});

function payClicked() {
    if ($('#id_type').val() === 'Credit') {
        handler.open({
            amount: parseFloat($('#id_amount').val()) * 100,
        });
    }
}// end payClicked()