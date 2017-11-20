$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('#edit_info').click(function() {
        $(this).css('display', 'none');
        $('#save_info').css('dispaly', 'inline');
        removeInfoReadOnlyAttributes();
    });
    $('#save_info').click(function() {
        $('#info_form').submit();
    });
    $('#edit_description').click(function() {
        $(this).css('display', 'none');
        $('#save_description').css('display', 'inline');
        $('#id_description').removeAttr('readonly');
    });
    $('#save_description').click(function() {
        $('#description_form').submit();
    });
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function removeInfoReadOnlyAttributes() {
    $('#id_first_name').removeAttr('readonly');
    $('#id_last_name').removeAttr('readonly');
    $('#id_city').removeAttr('readonly');
    $('#id_state').removeAttr('readonly');
    $('#id_education').removeAttr('readonly');
    $('#id_occupation').removeAttr('readonly');
    $('#id_other').removeAttr('readonly');
}// end removeInfoReadOnlyAttributes()