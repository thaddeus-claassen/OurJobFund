var current_num_searches = 0;
var finished_num_searches = 0;
var current_sort = 'date-descending';
var finished_sort = 'pledge-descending';

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    removeBorder();
    $('.table-header').click(function() {
        var cls = $(this).parent().attr('class');
        if (cls !== '') {
            setRowToZero(cls.split('-')[0]);
            prepareToAddRows(cls, 0);
        }// end if
    });
    $('tbody').scroll(function() {
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight) {
            var cls = $(this).attr('class');
            var table = cls.split('-')[0];
            var total = $('#' + table + '-total').text();
            if ($(this).children().count() < total) {
                if (cls !== '') {        
                    var rows = addToNumRows(cls);
                    prepareToAddRows(cls, rows);
                }// end if
            }// end if
        }// end if
    });
});

function removeBorder() {
    var user = $('#this_user').val();
    var detail_user = $('#username').text();
    if (user !== detail_user) {
        $('textarea').css('border', 'none');
    }// end if
}// end removeBorder()

function setSortVariable(table, type) {
    var sort = null;
    if (table === 'current') {
        if (type === current_sort.split('-')[0]) {
            if (current_sort.split('-')[1] === 'ascending') {
                current_sort = type + '-descending';
            } else {
                current_sort = type + '-ascending';
            }// end if-else
        } else {
            current_sort = type + '-ascending';
        }// end if-else
        sort = current_sort;
    } else if (table === 'finished') {
        if (type === finished_sort.split('-')[0]) {
            if (finished_sort.split('-')[1] === 'ascending') {
                finished_sort = type + '-descending';
            } else {
                finished_sort = type + '-ascending';
            }// end if-else
        } else {
            finished_sort = type + '-ascending';
        }// end if-else
        sort = finished_sort;
    }// end if
    return sort;
}// end setSortVariable()

function addToNumRows(table) {
    var rows;
    if (table === 'current') {
        current_num_searches = current_num_searches + 1;
        rows = current_num_searches;
    } else if (table === 'finished') {
        finished_num_searches = finished_num_searches + 1;
        rows = finished_num_searches;
    }// end if
    return rows;
}// end addToNumRows()

function setRowToZero(table) {
    if (table === 'current') {
        current_num_searches = 0;
    } else if (table === 'finished') {
        finished_num_searches = 0;
    }// end if
}// end setRowToZero()

function prepareToAddRows(cls, rows) {
    var table = cls.split('-')[0];
    var type = cls.split('-')[1];
    add_rows_to_tables(rows, table, type, setSortVariable(table, type).split('-')[1]);
}// end prepareToAddRows()

function getNumSearches(table) {
    var searches = null;
    if (table === 'current') {
        searches = current_num_searches;
    } else if (table === 'finished') {
        searches = finished_num_searches;
    }// end if
    return searches;
}// end getNumSearches();

function add_rows_to_tables(num_searches, table, column, order) {
    $.ajax({
        url : 'sort',
        data : {
            'num_searches' : num_searches,
            'table' : table,
            'column' : column,
            'order' : order,
        },
        success: function(json) {
            if (table === 'current') {
                if (current_num_searches == 0) $('#current tbody').empty();
                addRowsToCurrentTable(json);
            } else if (table === 'finished') {
                if (finished_num_searches == 0) $('#finished tbody').empty();
                addRowsToFinishedTable(json);
            }// end if
        },
    });
}// end sort()

function addRowsToCurrentTable(json) {
    for (var index = 0; index < json.length; index++) {
        var current = json[index];      
        var string = "<tr>";
        string = string + "<td class='current-title'><a href='/job/" + current['random_string'] + "'>" + current['title'] + "</a></td>";
        string = string + "<td class='current-pledging'>" + changeNumberToCurrency(current['pledging']) + "</td>";
        string = string + "<td class='current-paid'>" + changeNumberToCurrency(current['paid']) + "</td>";
        string = string + "<td class='current-received'>" + changeNumberToCurrency(current['received']) + "</td>";
        string = string + "</tr>";
        $('#current tbody').append(string);
    }// end for
}// end addRowsToCurrentTable()

function addRowsToCompletedTable(json) {
    for (var index = 0; index < json.length; index++) {
        var completed = json[index];
        var pledging, paid, work_status, received;
        if (current['pledging'] == 0) {
            pledging = "--";
            paid = "--";
            work_status = current['work_status'];
            received = changeNumberToCurrency(current['received']);
        } else {
            pledging = changeNumberToCurrency(current['pledging']);
            paid = changeNumberToCurrency(current['paid']);
            work_status = "--";
            received = "--"
        }// end if-else
        var string = "<tr>";
        string = string + "<td class='completed-title'><a href='/job/" + completed['random_string'] + "'>" + completed['title'] + "</a></td>";
        string = string + "<td class='completed-pledging'>" + pledging + "</td>";
        string = string + "<td class='completed-paid'>" + paid + "</td>";
        string = string + "<td class='completed-received'>" + received + "</td>";
        string = string + "</tr>";
        $('#completed tbody').append(string);
    }// end for
}// end addRowsToCompletedTable()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function changeNumberToCurrency(number) {
    var currency = null;
    var parts = number.toString().split('.');
    if (parts.length == 1) {
        currency = "$" + number + ".00";
    } else if (parts.length == 2) {
        if (parts[1].length == 2) {
            currency = "$" + number;
        } else {
            currency = "$" + number + "0";
        }// end if-else
    }// end if
    return currency;
}// end changeNumberToCurrencyFormat()
