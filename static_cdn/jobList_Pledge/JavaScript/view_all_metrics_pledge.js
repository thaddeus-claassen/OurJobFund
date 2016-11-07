$('document').ready(function() {
    $('text:input').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
        }// end if
    });    
});