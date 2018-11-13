var num_searches = 0;
var sort = 'date-descending';

$('document').ready(function() {
    fixHeader();
    $(window).resize(function() {
        fixHeader();
    });
    $('.table-header').click(function() {
        var cls = $(this).parent().attr('class');
        num_searches = 0;
        setSortVariable(cls);
        add_rows_to_tables();
    });
    $('tbody').scroll(function() {
        var cls = $(this).parent().attr('class');
        var total = parseInt($('#total').text());
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight && 50 * num_searches <= total) {
            if (cls !== '') {
                num_searches = num_searches + 1;
                add_rows_to_tables();
            }// end if
        }// end if
    });
});

function fixHeader() {
    var historyWidth = $('thead').width() - 17;
    $('thead').find('.username').width(0.2 * historyWidth - 16);
    $('thead').find('.date').width(0.16 * historyWidth - 16);
    $('thead').find('.type').width(0.16 * historyWidth - 16);
    $('thead').find('.amount').width(0.16 * historyWidth - 16);
    $('thead').find('.to').width(0.16 * historyWidth - 16);
    $('thead').find('.from').width(0.16 * historyWidth - 16);
    $('thead').find('.confirmed').width(0.16 * historyWidth + 1);
}// end fixHeader()

function setSortVariable(cls) {
    var col = sort.split("-")[0];
    var ascending_or_descending = sort.split("-")[1];
    if (col === cls) {
        if (ascending_or_descending === 'ascending') {
            sort = col + '-descending';
        } else {
            sort = col + '-ascending';
        }// end if-else
    } else {
        sort = cls + '-ascending';
    }// end if-else
}// end set_sort_variable()

function add_rows_to_tables(column, order) {
    $.ajax({
        url : 'sort',
        data : {
            'num_searches' : num_searches,
            'column' : sort.split("-")[0],
            'order' : sort.split("-")[1],
        },
        success: function(json) {
            if (json.length > 0) {
                addRowsToTable(json);
            };
        },
    });
}// end sort()

