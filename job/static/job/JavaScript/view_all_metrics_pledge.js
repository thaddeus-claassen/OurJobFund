
function getURL() {
    return 'view_all_metrics_pledge';
}// end getCopyMetricsURL()

function metricsCopiedSuccess(json) {
    $('#apply_someone_elses_metrics_span').text('Done!');
    $('#apply_someone_elses_metrics_span').css('color', 'blue');
    if (Object.keys(json).length > 0) {
        $('#id_inactive').val(json['inactive']);
        var inactive_unit = json['inactive_unit'];
        if (inactive_unit === 'day') {
            $('#id_inactive_unit_0').prop('checked', true);
        } else if (inactive_unit === 'week') {
            $('#id_inactive_unit_1').prop('checked', true);
        } else if (inactive_unit === 'month') {
            $('#id_inactive_unit_2').prop('checked', true);
        } else {
            $('#id_inactive_unit_3').prop('checked', true);
        }// end if-else
        $('#id_updated').val(json['updated']);
        var updated_unit = json['updated_unit'];
        if (updated_unit === 'day') {
            $('#id_updated_unit_0').prop('checked', true);
        } else if (updated_unit === 'week') {
            $('#id_updated_unit_1').prop('checked', true);
        } else if (updated_unit === 'month') {
            $('#id_updated_unit_2').prop('checked', true);
        } else {
            $('#id_updated_unit_3').prop('checked', true);
        }// end if-else
        $('#id_completed_fewer').val(json['completed_fewer']);
        $('#id_failed_to_complete').val(json['failed_to_complete']);
        $('#id_completed_percent').val(json['completed_percent']);
        $('#id_complted_ratio').val(json['completed_ratio']);
    }// end if
}// end metricsCopiedSuccess()

function clearMetrics() {
    $(':text').val('');
    $('#inactive_day').prop('checked', true);
    $('#updated_day').prop('checked', true);
    $.ajax({                                                                                                              
        type : "POST",                                                          
        url : "clear_metrics",                                           
        data : {
            'pledge_or_worker' : 'pledge-page-worker-database', 
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        }                                                                                             
    });
}// end clearMetrics()

function homeURL() {
    return 'pledge';
}// end returnToHome()

