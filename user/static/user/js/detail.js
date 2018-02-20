$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    disableInfo();
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function disableInfo() {
    if ($('#this_user').val() !== $('#username').text()) {
        $('#id_first_name').attr('readonly', true);
        $('#id_last_name').attr('readonly', true);
        $('#id_city').attr('readonly', true);
        $('#id_state').attr('disabled', true);
        $('#id_education').attr('readonly', true);
        $('#id_occupation').attr('readonly', true);
        $('#id_contact').attr('readonly', true);
        $('#id_description').attr('readonly', true);
    }// end if
}// end disableInfo()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()