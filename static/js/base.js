var canSubmit = true;

$('document').ready(function() {
    $('#go_to_user').submit(function(event) {
        if (canSubmit) {       
            if ($('#user_search_bar').val() === "") {
                event.preventDefault();
            } else {
                canSubmit = false;
            }// end if-else
        } else {
            event.preventDefault()
        }// end if-else
    });
});