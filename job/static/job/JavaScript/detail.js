var currSort = "date_descending";

$('document').ready(function() {
    $('.sort').click(function() {
        $('tbody').each(function(i, obj) {
            $(this).css('display', 'none');
        });
        sortArray = currSort.split("_");
        if ($(this).attr('id') === sortArray[0] && sortArray[1] === 'ascending') {
            currSort = $(this).attr('id') + "_descending";
        } else {
            currSort = $(this).attr('id') + "_ascending";
        }// end if-else
        $('#' + currSort).css('display', 'inline');
    });
    $('#pledge_money').click(function() {
        $(this).css('display', 'none');
        $('.pledge_clicked').css('display', 'inline');
    });
    $('#pay_money').click(function() {
        $(this).css('display', 'none');
        $('#pay_clicked').css('display', 'inline');
    });
    $('#work_on_job').click(function() {
        if ($(this).attr('type') === 'button') {
            $(this).css('display', 'none');
            $('#connect_with_stripe_message').css('display', 'inline');
            $('#stripe_connect').css('display', 'inline');
        }// end if
    });
    $('.pay_worker').click(function() {
        $(this).css('display', 'none');
        var name = $(this).attr('id').split('_');
        $('#paying_' + name[1]).css('display', 'inline');
    });
    var handler = StripeCheckout.configure({
        key: 'pk_test_DF7zGC0IPpcOQyWr2nWHVLZ6',
        locale: 'auto',
        name: 'OurJobFund',
        description: 'One-time donation',
        token: function(token) {
            $('#stripe_token').val(token.id);
            $('#pay_form').submit();
        }
    });
    $('.pay_button').click(function(e) {
        e.preventDefault();
        $('#error_explanation').html('');
        var username = $(this).attr('id').split("-")[0];
        var amount = $('#' + username + '-amount_paying').val();
        amount = amount.replace(/\$/g, '').replace(/\,/g, '')
        amount = parseFloat(amount);
        if (isNaN(amount)) {
            $('#error_explanation').html('<p>Please enter a valid amount in USD ($).</p>');
        } else if (amount < 5.00) {
            $('#error_explanation').html('<p>Donation amount must be at least $1.</p>');
        } else {
            amount = Math.round(amount * 100); // Needs to be an integer!
            $('#pay_amount').val(amount);
            $('#pay_to').val(username);
            handler.open({
                amount: amount
            });
        }
    });
    // Close Checkout on page navigation
    $(window).on('popstate', function() {
        handler.close();
    });
});

function correctFormat() {
    var errorMessage = "";
    var amount = parseFloat($('#pledge_amount').val());
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

function pledge_money_to_job() {
    $.ajax({
        type : "POST",
        url : "" + $('#job-id').text() + "/pledge_money_to_job",
        data : {
            'amount_pledged' : $('#pledge_amount').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : pledgingMoneyToJobSuccess,
    });
}// end pledge_money()

function pledgingMoneyToJobSuccess(string) {
    $('#will-you-pledge-money-to-job').css('display', 'none');
    $('#you-are-pledging').css('display', 'inline');
    var row = "<tr>";
    row += "<td>" + string.split(" ")[0] + "</td>";
    row += "<td>Pledge: $" + string.split(" ")[1] + "</td>";
    row += "<td>Paid: $0.0</td></tr>";
    $('#pledges_table').prepend(row);
}// end pledgingMoenyToJobSuccess()

function workOnJobSuccess(string) {
    if (string == 'success') {

    }// end if
}// end workOnJobSuccess()















