var orgFirstName; 
var orgLastName;
var orgCity;
var orgState;
var orgOccupation;
var orgEducation;
var orgContact;
var orgDescription;

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    initInfoAndDescription();
    initMustConnectToString();
    $('#edit_info').click(function() {
        removeReadonlyInfoAttributes();
        $('#edit_info').css('display', 'none');
        $('#save_info').css('display', 'inline');
        $('#cancel_info').css('display', 'inline');
    });
    $('#cancel_info').click(function() {
        addReadonlyInfoAttributes();
        $('#edit_info').css('display', 'inline');
        $('#save_info').css('display', 'none');
        $('#cancel_info').css('display', 'none');
        cancelInfo();
    });
    $('#save_info').click(function() {
        $('#info_form').submit();
    });
    $('#edit_description').click(function() {
        removeReadonlyDescriptionAttributes();
        $('#edit_description').css('display', 'none');
        $('#save_description').css('display', 'inline');
        $('#cancel_description').css('display', 'inline');
    });
    $('#cancel_description').click(function() {
        addReadonlyDescriptionAttributes();
        $('#edit_description').css('display', 'inline');
        $('#save_description').css('display', 'none');
        $('#cancel_description').css('display', 'none');
        $('#id_description').text(); 
    });
    $('#save_description').click(function() {
        $('#description_form').submit();
    });
    $('#id_preferred_payment').change(function() {
        if ($(this).val() === "ANY" | $(this).val() === "CREDIT") {
            $('#must-connect-to-stripe').css('display', 'inline');
        } else {
            $('#must-connect-to-stripe').css('display', 'none');
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
            $('#pay_form').submit();
        }
    });
    $('#pay_button').click(function(e) {
        $('#pay_for_error').text('');
        var job = $('#pay_for').val();
        if (job === "(default)") {
            $('#pay_for_error').text('Please select a job.');
        } else {
            $('#pay_amount_error').text('');
            var amount = $('#pay_amount').val();
            amount = parseFloat(amount);
            if (isNaN(amount)) {
                $('#pay_amount_error').text('Please enter a valid amount in USD ($).');
            } else if (amount < 0.5) {
                $('#pay_amount_error').text('Payment must be at least $0.50.');
            } else {
                amount = Math.round(amount * 100); // Needs to be an integer!
                if (Math.floor(amount) === amount) {
                    handler.open({
                        amount: amount,
                    });
                } else {
                    $('#pay_amount_error').text('Please enter a valid amount in USD ($).');
                }// end if-else
            }// end if-else
        }// end if-else
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
}

function initMustConnectToString() {
    if ($('#id_preferred_payment').val() === "ANY" | $('#id_preferred_payment').val() === "CREDIT") {
        $('#must-connect-to-stripe').css('display', 'inline');
    } else {
        $('#must-connect-to-stripe').css('display', 'none');
    }// end if-else
}// end initMustConnectToString()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function initInfoAndDescription() {
    orgFirstName = $('#id_first_name').val();
    orgLastName = $('#id_last_name').val();
    orgCity = $('#id_city').val();
    orgState = $('#id_state').val();
    orgOccupation = $('#id_occupation').val();
    orgEducation = $('#id_education').val();
    orgContact = $('#id_contact').val();
    orgDescription = $('#id_description').val();
    addReadonlyInfoAttributes();
    addReadonlyDescriptionAttributes();
}// end initInfoAndDescription()

function cancelInfo() {
    $('#id_first_name').val(orgFirstName);
    $('#id_last_name').val(orgLastName);
    $('#id_city').val(orgCity);
    $('#id_state').val(orgState);
    $('#id_occupation').val(orgOccupation);
    $('#id_education').val(orgEducation);
    $('#id_contact').val(orgContact);
}// end cancelInfo()

function cancelDescription() {
    $('#id_description').val(orgDescription);
}// end cancelDescription()

function removeReadonlyInfoAttributes() {
    $('.info').each(function(index) {
        if ($(this).attr('type') === 'text') {
            $(this).removeAttr('readonly');
        } else {
            $(this).removeAttr('disabled');
        }// end if-else
    });
}// end removeReadOnlyAttributes()

function addReadonlyInfoAttributes() {
    $('.info').each(function(index) {
        if ($(this).attr('type') === 'text') {
            $(this).prop('readonly', true);
        } else {
            $(this).prop('disabled', true);
        }// end if-else
    });
}// end addReadonlyInfoAttributes()

function removeReadonlyDescriptionAttributes() {
    $('#id_description').removeAttr('readonly');
}// end removeReadOnlyDescriptionAttributes()

function addReadonlyDescriptionAttributes() {
    $('#id_description').prop('readonly', true);
}// end addReadonlyDescriptionAttributes()

function mustConnectToStripe() {
    $('#must-connect-to-stripe')
}// end mustConnectToStripe()