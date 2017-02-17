
function getURL() {
    return 'view_all_metrics_work';
}// end getCopyMetricsURL()

function copy_metrics() {
    $.ajax ({
        type : 'POST',
        url : 'copy_worker_metrics',
        data : {
            'username' : $('#apply_someone_elses_metrics_text').val(),
        },
        success : metricsCopiedSuccess,
    });
}// end copy_pledge_metrics()

function metricsCopiedSuccess(json) {
    $('#apply_someone_elses_metrics_span').text('Done!');
    $('#apply_someone_elses_metrics_span').css('color', 'blue');
    if (Object.keys(json).length > 0) {
        $('#id_inactive').val(json['inactive']);
        var unit = json['inactive_unit'];
        if (unit === 'day') {
            $('#id_inactive_unit_0').prop('checked', true);
        } else if (unit === 'week') {
            $('#id_inactive_unit_1').prop('checked', true);
        } else if (unit === 'month') {
            $('#id_inactive_unit_2').prop('checked', true);
        } else {
            $('#id_inactive_unit_3').prop('checked', true);
        }// end if-else
        $('#id_failed_to_pay').val(json['failed_to_pay']);
        $('#id_averaged').val(json['failed_to_pay']);
        $('#id_paid_x_times').val(json['paid_x_times']);
    }// end if
}// end metricsCopiedSuccess()

function clearMetrics() {
    $(':text').val('');
    $('#updated_day').prop('checked', true);
    $.ajax({                                                                                                              
        type : "POST",                                                          
        url : "clear_metrics",                                           
        data : {
            'pledge_or_worker' : 'work-page-pledge-database', 
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        }                                                                                             
    });
}// end clearMetrics()

function homeURL() {
    return 'work';
}// end returnToHome()