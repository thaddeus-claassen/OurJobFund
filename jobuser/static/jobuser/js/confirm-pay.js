var canSubmit = true;

$(document).ready(function() {
    $('#form').submit(function(e) {
        if (canSubmit) {
            canSubmit = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
});