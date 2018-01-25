$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    disableInfo();
    $('#pay_button').click(function() {
        var result = checkPayAmountFormat();
        if (result === 'no error'){
            handler.open({
                amount: amount,
            });
        } else  {
            $('#amount_error').text(result);
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

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function disableInfo() {
    if ($('#this_user').val() !== $('#username').text()) {
        $('#id_first_name').attr('readonly', true);
        $('#id_last_name').attr('readonly', true);
        $('#id_city').attr('readonly', true);
        $('#id_state').attr('disabled', true);
        $('#id_education').attr('readonly', true);
        $('#id_occupation').attr('readonly', true);
        $('#id_contact').attr('readonly', true);
        $('#id_description').attr('readonly', true);
    }// end if
    if ($('#pay_for').children('option').length == 1) {
        $('#pay_unclicked').css('display', 'none');
    }// end if
}// end disableInfo()

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

function checkPayAmountFormat() {
    var result = "";
    $('#amount_error').text('');
    var amount = $('#pay_amount').val();
    amount = parseFloat(amount);
    if (isNaN(amount)) {
        result = 'Please enter a valid amount in USD ($).';
    } else if (amount < 0.5) {
        result = 'Payment must be at least $0.50.';
    } else {
        amount = Math.round(amount * 100); // Needs to be an integer!
        if (Math.floor(amount) === amount) {
            result = "no error";
        } else {
            result = 'Please enter a valid amount in USD ($).';
        }// end if-else
    }// end if-else
    return result;
}// end checkPayAmountFormat()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()