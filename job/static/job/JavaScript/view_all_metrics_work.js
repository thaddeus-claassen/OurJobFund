
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