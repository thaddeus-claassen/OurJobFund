$('document').ready(function() {
    disableInputs();
    $('.edit').click(function() {
        var action = $(this).attr('id').split('_')[0];
        if (action !== 'save') {
            $(this).css('display', 'none');
            var info = $(this).attr('id').split('_')[1];
            if (action === 'change') {
                if (info === 'password') {
                    $('input[type=password]').removeAttr('disabled');
                } else {
                    $('#id_' + info).removeAttr('disabled');
                }// end if-else
                $('#save_' + info).css('display', 'inline');
                $('#cancel_' + info).css('display', 'inline');
            } else if (action === 'cancel') {
                if (info === 'password') {
                    $('input[type=password]').prop('disabled', true);
                } else {
                    $('#id_' + info).prop('disabled', true);
                }// end if-else
                $('#save_' + info).css('display', 'none');
            }// end if
        }// end if
    });
    $('#deactivate-account').click(function() {
        $(this).css('display', 'none');
        $('.deactivate').css('display', 'inline');        
    });
    $('#cancel-deactivate-account').click(function() {
        $('#deactivate-account').css('display', 'inline');
        $('.deactivate').css('display', 'none');
    });
});

function disableInputs() {
    $('#id_username').prop('disabled', true);
    $('#id_email').prop('disabled', true);
    $('input[type=password]').prop('disabled', true);
}// end disableInputs()


