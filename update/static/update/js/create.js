var canSubmit = true;

$(document).ready(function() {
    $('#form').submit(function(e) {
        var type = $('#submit_button').attr('name').split('_')[1];
        format = correctFormat(type);
        if (format === "") {
            if (type === 'pay') {
                if (canSubmit) {
                    payClicked();
                    canSubmit = false;
                    e.preventDefault();
                }// end if
            } else {
                if (canSubmit) {
                    canSubmit = false; 
                } else {
                    e.preventDefault();
                }// end if-else
            }// end if-else
        } else {
            $('#amount-error-message').remove();
            $('#id_amount').after("&nbsp;&nbsp;&nbsp;<span id='amount-error-message'>" + format + "</span>");
            e.preventDefault();
        }// end if-else
    });
});