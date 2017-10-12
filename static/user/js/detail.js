$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('#edit_info').click(function() {
        $('.no-change-info-wrapper').css('display', 'none');
        $('.change-info-wrapper').css('display', 'inline');
    });
    $('#edit_description').click(function() {
        $('.no-change-description-wrapper').css('display', 'none');
        $('.change-description-wrapper').css('display', 'inline');
    });
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

