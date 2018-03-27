var canSubmit = true;

$('document').ready(function() {
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }// end if
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