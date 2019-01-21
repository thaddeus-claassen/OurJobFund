var canSubmit = true;

$('document').ready(function() {
    $('#form').submit(function(event) {
        format = correctFormat();
        if (format === "") {
            if (canSubmit) {
                canSubmit = false;
                formContent();
            } else {
                event.preventDefault();
            }// end if-else
        } else {
            errorMessage();
            event.preventDefault();
        }// end if-else
    });
    $('#back-button').submit(function(event) {
        if (canSubmit) {
            canSubmit = false;
        } else {
            event.preventDefault();
        }// end if-else
    });
});

function correctFormat() {return ""}