$('document').ready(function() {
    // CKEDITOR.replace( 'editor1' );
    $('label:text').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
        }// end if
    });
    $('label:textarea').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
        }// end if
    });
});