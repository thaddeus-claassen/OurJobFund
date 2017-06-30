$('document').ready(function() {
    $('#make_edits').click(function() {
        makeEdits();
    });
    $('#edit_description').click(function() {
        $('#edit_description').css('display', 'none')
        $('#description_div').css('display', 'none');
        $('#textarea_description').css('display', 'inline');
        $('#textarea_description').text($('#description').text());
        $('#save_description').css('display', 'inline');
    });
    $('#save_description').click(function() {
        description();
        $('#description_div').css('display', 'inline');
        $('#description').text($('#textarea_description').val());
        $('#textarea_description').css('display', 'none');
        $('#save_description').css('display', 'none');
        $('#edit_description').css('display', 'inline');
    });
});

function description() {
    $.ajax({
        type : "POST",
        url : "description/",
        data : {
            'description' : $('#textarea_description').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end save_description()

function makeEdits() {
    $('#make_edits_button_div').css('display', 'none');
    $('#edit_div').css('display', 'inline');
}// end makeEdits()

