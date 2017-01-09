var originalText;
var opacity = 0.75;
$('document').ready(function() {
    originalText = $('#custom-logic').val();
    $('#custom-logic').css('opacity', opacity);
    $('#custom-logic').focusout(function() {
       if ($('#custom-logic').val() == "") {
           $('#custom-logic').val(originalText);
           $('#custom-logic').css('opacity', opacity);
       }// end if
    });
    $('#custom-logic').focus(function() {
        if ($('#custom-logic').val() == originalText && $('#custom-logic').css('opacity') == opacity) {
            $('#custom-logic').css('opacity', 10);
            $('#custom-logic').val("");
        }// end if
    });
    $(':button').click(function() {
        //window.close();
    });
});