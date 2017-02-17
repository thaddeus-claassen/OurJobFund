$('document').ready(function() {
    $('#apply_someone_elses_metrics').click(function() {
        verify_username();
    });
    $('#apply-metrics-form').submit(function(event) {
        var errorMessages = showErrorMessages();
        if (errorMessages) {
            event.preventDefault();
        }// end if
    });
    $('#clear_metrics').click(function() {
        clearMetrics();
    });
    $('#cancel_metrics').click(function() {
        document.location = '/job/' + homeURL() + '/'
    });
});

function verify_username() {
    $.ajax ({
        type : 'GET',
        url : 'verify_username',
        data : {
            'username' : $('#apply_someone_elses_metrics_text').val(),
        },
        success : verifyUsernameSuccess,
    });
}// end verify_username()

function verifyUsernameSuccess(str) {
    if (str === 'true') {
        copy_metrics();
    } else {
        $('#apply_someone_elses_metrics_span').text('Username does not exist');
        $('#apply_someone_elses_metrics_span').css('color', 'red');
    }// end if-ese
}// end verrifyUsernameSuccess()

function copy_metrics() {
    $.ajax ({
        type : 'POST',
        url : 'copy_pledge_metrics',
        data : {
            'username' : $('#apply_someone_elses_metrics_text').val(),
        },
        success : metricsCopiedSuccess,
    });
}// end copy_metrics
