var canSubmit = true;

$(document).ready(function() {
    $('#post_update_form').submit(function(e) {
        if (canSubmit) {
            canSubmit = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
});