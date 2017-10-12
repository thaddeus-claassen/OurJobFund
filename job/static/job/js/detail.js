var currSort = 'date-descending';

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('.sort').click(function() {
        sort($(this).attr('id'));
    });
    $('#pledge_money').click(function() {
        $(this).css('display', 'none');
        $('#pledge-money-form').css('display', 'inline');
    });
    $('#cancel-pledge-money').click(function() {
        $('#pledge_money').css('display', 'inline');
        $('#pledge-money-form').css('display', 'none');
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

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function sort(sort) {
    ascending_or_descending = 'ascending';
    if (sort === currSort.split('-')[0] && currSort.split('-')[1] === 'ascending') {
        ascending_or_descending = 'descending';
    }// end if
    currSort = sort + "-" + ascending_or_descending;
    $.ajax({
        url : $(location).attr('href') + "sort",
        data : {
            'sort' : sort,
            'ascending_or_descending' : ascending_or_descending,
        },
        success: sortSuccess,
    });
}// end sort()

function sortSuccess(json) {
    //$('#update-body').empty();
    //var num = Object.keys(json).length;
    //if (num > 0) {
    //    for (var index = 0; index < json.length; index++) {
    //        var update = json[index];
    //        var fields = job["fields"];
    //    }// end for
    //}// end if
}// end sortSuccess()

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

















