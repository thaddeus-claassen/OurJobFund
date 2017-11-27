$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    if ($('#this_user').val() === $('#username').text()) {
        removeReadOnlyAttributes()
    }// end if
    $('#save_info').click(function() {
        $('#info_form').submit();
    });
    $('#save_description').click(function() {
        $('#description_form').submit();
    });
    alert("offset.top: " + $('#id_other').offset().top);
    alert("outerheight: " + $('#id_other').outerHeight(false));
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function setHeightOfOther() {
    
}// end setHeightOfOther()

function removeReadOnlyAttributes() {
    $('#id_description').removeAttr('readonly');
    $('#id_first_name').removeAttr('readonly');
    $('#id_last_name').removeAttr('readonly');
    $('#id_city').removeAttr('readonly');
    $('#id_state').removeAttr('disabled');
    $('#id_education').removeAttr('readonly');
    $('#id_occupation').removeAttr('readonly');
    $('#id_other').removeAttr('readonly');
}// end removeReadOnlyAttributes()