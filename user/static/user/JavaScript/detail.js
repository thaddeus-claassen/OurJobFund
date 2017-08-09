$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
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
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function save_description() {
    $.ajax({
        type : "POST",
        url : "description/",
        data : {
            'description' : $('#textarea_description').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : saveDescriptionSuccess,
    });
}// end save_description()

function saveDescriptionSuccess() {
    $('#description_div').css('display', 'inline');
    $('#description').text($('#textarea_description').val());
    $('#edit_description').css('display', 'inline');
    $('#textarea_description').css('display', 'none');
    $('#save_description').css('display', 'none');
}// end saveDescriptionSuccess()

function makeEdits() {
    $('#make_edits_button_div').css('display', 'none');
    $('#edit_div').css('display', 'inline');
}// end makeEdits()

