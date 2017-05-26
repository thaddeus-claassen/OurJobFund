$('document').ready(function() {
    $('#view-description').click(function(event) {
        event.preventDefault();
        var jobID = $(this).attr('class');    
        window.open("/job/" + jobID + "/description");
    });
    $('#will_you_pledge_money').click(function() {
        $('#pledge_modal').css('display', 'inline');
    });
    $('#modal_make_pledge').click(function() {
        var errorMessage = correctFormat()
        if (errorMessage === "") {
            pledge_money_to_job();
            $('#pledge_modal').css('display', 'none');
            $('#will_you_pledge_money').css('display', 'none');
            $('#will_you_pledge_money').after('You are pledging $' + $('#pledge_amount').val());
        } else {
            $('#pledge_error_message').text(errorMessage);
            $('#pledge_error_message').css('color', 'red');
        }// end if-else
    });
    $('#finish_job').click(function() {
        $('#finish_modal').css('display', 'inline');
    });
    $('.finish-yes-no').click(function() {
        css('display', 'none');
    });
    $('.close_modal').click(function() {
        $('#pledge_modal').css('display', 'none');
    });
    $('#work_on_job').click(function() {
        $('#work_on_job').css('display', 'none');
        work_on_job();
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

function work_on_job() {
    $.ajax({
        type : "POST",
        url : "work_on_job",
        data : {
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : workOnJobSuccess,
    });
}// end work_on_job()

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















