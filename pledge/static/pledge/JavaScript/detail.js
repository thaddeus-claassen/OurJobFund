$('document').ready(function() {
    user_is_pledging_money();
    user_is_working_on_job();
    $('#view-description').click(function(event) {
        event.preventDefault();
        var jobID = $(this).attr('class');    
        window.open("/pledge/" + jobID + "/description");
    }); 
    $('will-you-pledge-money').click(function()) {
        pledge_money();
    }// end will-you-pledge-money()
    $('#decide-to-work-on-job').click(function() {
        work_on_job();
    });
});

function user_is_pledging_money() {
    $.ajax({
        type : "GET",
        url : "" + $('#job-id').text() + "/user_is_pledging_money",
        success : pledgingMoneyToJobSuccess,
    });
}// end user_is_pledging_money()

function user_is_working_on_job() {
    $.ajax({
        type : "GET",
        url : "" + $('#job-id').text() + "/user_is_working_on_job",
        success : workingOnJobSuccess,
    });  
}// end user_is_working_on_job()

function work_on_job() {
    $.ajax({
        type : "POST",
        url : "" + $('#job-id').text() + "/work_on_job",
        data : {
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : workOnJobSuccess,
    });
}// end work_on_job()

function pledgingMoneyToJobSuccess(string) {
    if (string == '') {
        $('#will-you-pledge-money-to-job').css('display', 'inline');
        $('#you-are-pledging').css('display', 'none');
        $('#you-are-pledging-amount').css('display', 'none');
    } else {
        $('#will-you-pledge-money-to-job').css('display', 'none');
        $('#you-are-pledging').css('display', 'inline');
        $('#you-are-pledging-amount').css('display', 'inline');
        $('#you-are-pledging-amount').text(string);
    }// end if-else
}// end pledgingMoenyToJobSuccess()

function workingOnJobSuccess(string) {
    if (string == 'Exists') {
        $('#decide-to-work-on-job').css('display', 'none');
        $('#you-are-working-on-the-job').text('You are working on the job');
    }// end if
}// end workOnJobSuccess()

function workOnJobSuccess(string) {
    if (string == 'Exists') {
        $('#decide-to-work-on-job').css('display', 'none');
        $('you-are-working-on-the-job').text('&#2714; Now you are working on the job');
    }// end if
}// end workOnJobSuccess()
