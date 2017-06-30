var currSort = "date_descending";

$('document').ready(function() {
    $('.sort').click(function() {
        $('tbody').each(function(i, obj) {
            $(this).css('display', 'none');
        });
        //sortArray = currSort.split("_");
        //if ($(this).attr('id') === sortArray[0] && sortArray[1] === 'ascending') {
        //    currSort = $(this).attr('id') + "_descending";
        //} else {
        //    currSort = $(this).attr('id') + "_ascending";
        //}// end if-else
        //$('#' + currSort).css('display', 'inline');
        $('#title_ascending').css('display', 'inline');
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















