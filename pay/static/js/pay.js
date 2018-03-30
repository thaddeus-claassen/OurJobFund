var canSubmit = true;

$('document').ready(function() {
    $('#form').submit(function() {
        if (canSubmit) {
            canSubmit = false;
        } else {
            event.preventDefault();
        }// end if-else
    });
});