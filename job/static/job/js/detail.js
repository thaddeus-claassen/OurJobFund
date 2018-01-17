var canSubmitPledge = true;
var canSubmitWork = true;
var currSort = 'date-descending';

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('.sort').click(function() {
        sort($(this).attr('id'));
    });
    $('#pay_money').click(function() {
        $('#pay_unclicked').css('display', 'none');
        $('#pay_clicked').css('display', 'inline');
    });
    $('#cancel_pay').click(function() {
        $('#pay_clicked').css('display', 'none');
        $('#pay_unclicked').css('display', 'inline');
    });
    $('#work_on_job').click(function() {
        if ($(this).attr('type') === 'button') {
            $(this).css('display', 'none');
            $('#connect_with_stripe_message').css('display', 'inline');
            $('#stripe_connect').css('display', 'inline');
        }// end if
    });
    $('#pledge-money-form').submit(function(e) {
        if (canSubmitPledge) {
            canSubmitPledge = false;
        } else {
            e.preventDefault();;
        }// end if-else
    });
    $('#work-form').submit(function(e) {
        if (canSubmitWork) {
            canSubmitWork = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
    $('#finish-form').submit(function(e) {
        if (canSubmitWork) {
            canSubmitWork = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
    $('#unfinish-form').submit(function(e) {
        if (canSubmitWork) {
            canSubmitWork = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
    togglePledgeWrapper();
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















