$('document').ready(function() {
    $('#apply_metrics').click(function() {
        applyMetrics();
        //document.location.href = 'index';
    });
    $('#clear_metrics').click(function() {
        clearMetrics();
    });
    $('#cancel_metrics').click(function() {
        document.location.href = 'index';
    });
});

function applyMetrics() {
    $.ajax({                                                                                                              
        type : "POST",                                                          
        url : "apply_metrics_pledge",                                           
        data : {
            'inactive' : getInactiveInput(),
            'inactive_unit_of_time' : getInactiveUnitOfTimeRadio(),
            'not-updated' : getNotUpdatedInput(),
            'updated-unit-of-time' : getUpdatedUnitOfTimeRadio(),
            'completed-fewer' : getCompletedFewerInput(),
            'failed-to-complete' : getFailedToCompleteInput(),
            'completed-percent' : getCompletedPercent(),
            'completed-ratio' : getCompletedRatio(),
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

function getNotUpdatedInput() {
    return $('#not-updated').val();
}// end getNotUpdatedInput()

function getUpdatedUnitOfTimeRadio() {
    var string;
    var id = $('input[name=updated_unit_of_time]:checked').attr('id');
    if (id == 'updated_day') string = 'day';
    else if (id == 'updated_week') string = 'week';
    else if (id == 'updated_month') string = 'month';
    else string = 'year';
    return string;
}// end getupdatedUnitOfTimeRadio()

function getCompletedFewerInput() {
    return $('#completed-fewer').val();
}// end getCompletedFewerInput()

function getFailedToCompleteInput() {
    return $('#failed-to-complete').val();
}// end getFailedToCompleteInput()

function getCompletedPercent() {
    var returnValue;
    var percent = $('#completed-percent').val();
    if (percent >= 0 && percent <= 100) {
        returnValue = percent;
    } else {
        returnValue = null;
    }// end if-else
    return returnValue;
}// end getCompletedPercent()

function getCompletedRatio() {
    var returnValue = $('#completed-ratio').val();
    if (returnValue < 0) returnValue = null;
    return returnValue;
}// end getCompletedRatio()

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





