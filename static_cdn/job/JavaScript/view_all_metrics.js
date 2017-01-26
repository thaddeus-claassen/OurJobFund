$('document').ready(function() {
    $('#apply-metrics-form').submit(function(event) {
        event.preventDefault();
        var errorMessages = showErrorMessages();
        event.preventDefault();
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

