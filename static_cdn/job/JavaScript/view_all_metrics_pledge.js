
function showErrorMessages() {
    var existErrorMessages = false;
    if (inactiveInputError()) {
        existErrorMessages = true;
        inactiveInputErrorMessage();
    }// end if
    if (notUpdatedInputError()) {
        existErrorMessages = true;
        notUpdatedInputErrorMessage();
    }// end if
    if (completedFewerInputError()) {
        existErrorMessages = true;
        completedFewerInputErrorMessage();
    }// end if
    if (failedToCompleteInputError()) {
        existErrorMessages = true;
        failedToCompleteInputErrorMessage();
    }// end if
    if (completedPercentInputError()) {
        existErrorMessages = true;
        completedPercentInputErrorMessage();        
    }// end if
    if (completedRatioInputError()) {
        existErrorMessages = true;
        completedRatioInputErrorMessage();        
    }// end if
    return existErrorMessages;
}// end if

function inactiveInputError() {
    alert("Inside inactiveInputError()");
    var error;
    var value = $('#inactive').val();
    alert("isInt(value) : " + isInt(value));
    alert("Number(value) : " + Number(value));
    alert("value % 1 === 0 : " +  value % 1 === 0);
    if (value != null && isInt(value)) {
        error = false;
    } else {
        error = true;
    }// end if-else
    alert("Error: " + error);
    return error;
}// end inactiveInputError

function inactiveInputErrorMessage() {
    $('#inactive').css('color', 'red');
}// end inactiveInputErrorMessage()

function notUpdatedInputError() {
    var error;
    var value = $('#not-updated').val();
    if (value != null && value === parseInt(value, 10)) {
        error = false;
    } else {
        error = true;
    }// end if-else
    return error;
}// end notUpdatedInputError()

function notUpdatedInputErrorMessage() {
    $('#not-updated').css('color', 'red');
}// end notUpdatedInputErrorMessage()

function completedFewerInputError() {
    var error;
    var value = $('#completed-fewer').val();
    if (value != null && value === parseInt(value, 10)) {
        error = false;
    } else {
        error = true;
    }// end if-else
    return error;
}// end completedFewerInputError()

function completedFewerInputErrorMessage() {
    $('#completed-fewer').css('color', 'red');
}// end completedFewerInputErrorMessage()

function failedToCompleteInputError() {
    var error;
    var value = $('#failed-to-complete').val();
    if (value != null && value === parseInt(value, 10) >= 0) {
        error = false;
    } else {
        error = true;
    }// end if-else
    return error;
}// end failedToCompleteInputError()

function failedToCompleteInputErrorMessage() {
    $('#failed-to-complete').css('color', 'red');
}// end failedToCompleteInputErrorMessage()

function completedPercentInputError() {
    var error;
    var value = $('#completed-percent').val();
    if (value != null && value === Number(value) && value >= 0 && value <= 100) {
        error = false;
    } else {
        error = true;
    }// end if-else
    return error;
}// end completedPercentInputError()

function completedPercentInputErrorMessage() {
    $('#completed-percent').css('color', 'red');
}// end completedPercentInputErrorMessage()

function completedRatioInputError() {
    var error;
    var value = $('#completed-ratio').val();
    if (value != null && value === Number(value) && value > 0) {
        error = false;
    } else {
        error = true;
    }// end if-else
    return error;
}// end completedRatioInputError()

function completedRatioInputErrorMessage() {
    $('#completed-ratio').css('color', 'red');
}// end completedRatioInputErrorMessage()

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

function isInt(n){
    return (Number(n) === n && n % 1 === 0);
}// end isInt()





