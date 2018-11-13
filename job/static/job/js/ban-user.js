$('document').ready(function() {
    fixHeader();
    $(window).resize(function() {
        fixHeader();
    });
});

function fixHeader() {
    var width = $('thead').width() - 17;
    $('thead').find('.date').width(0.25 * width - 16);
    $('thead').find('.type').width(0.25 * width - 16);
    $('thead').find('.amount').width(0.25 * width - 16);
    $('thead').find('.to').width(0.25 * width + 1);
}// end fixHeader()