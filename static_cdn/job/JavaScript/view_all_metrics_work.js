
function applyMetrics() {
    $.ajax({                                                                                                              
        type : "POST",                                                          
        url : "apply_metrics_work",                                           
        data : {
            'inactive' : getInactiveInput(),
            'inactive_unit_of_time' : getInactiveUnitOfTimeRadio(),
            'failed_to_pay' : getFailedToPay(),
            'averaged' : getAveraged(),
            'paid_x_times' : getPaidXTimes(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        }                                                                                             
    });
}// end applyMetrics()

function getInactiveInput() {
    return $('#inactive').val()
}// end getInactiveInput()

function getInactiveUnitOfTimeRadio() {
    var string;
    var id = $('input[name=inactive_unit_of_time]:checked').attr('id');
    if (id == 'inactive_day') string = 'day';
    else if (id == 'inactive_week') string = 'week';
    else if (id == 'inactive_month') string = 'month';
    else string = 'year';
    return string;
}// end getInactiveUnitOfTimeRadio()

function getFailedToPay() {
    return $('#failed-to-pay').val();
}// end getFailedToPay()

function getAveraged() {
    return $('#averaged').val();
}// end getAveraged()

function getPaidXTimes() {
    return $('#paid-x-times').val();
}// end getPaidXTimes()

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