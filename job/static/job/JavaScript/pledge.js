
function copy_metrics() {
    $.ajax ({
        type : 'POST',
        url : 'copy_pledge_metrics',
        data : {
            'username' : $('#apply_metrics_text').val(),
        },
        success : metricsCopiedSuccess,
    });
}// end copy_pledge_metrics()

function metricsCopiedSuccess(json) {
    $('#apply_metrics_span').text('Done!');
    $('#apply_metrics_span').css('color', 'blue');
    var numJobs = Object.keys(json).length; 
    if (numJobs > 0) {
        $('#inactive').val(json['inactive']);
        var unit = json['inactive_unit'];
        if (unit === 'day') {
            $('#inactive_day').prop('checked', true);
        } else if (unit === 'week') {
            $('#inactive_week').prop('checked', true);
        } else if (unit === 'month') {
            $('#inactive_month').prop('checked', true);
        } else {
            $('#inactive_year').prop('checked', true);
        }// end if-else
        $('#completed_fewer').val(json['completed_fewer']);
        $('#failed_to_complete').val(json['failed_to_complete']);
    }// end if
}// end metricsCopiedSuccess()



