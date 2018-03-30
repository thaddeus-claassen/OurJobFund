var canSubmitPledge = true;
var canSubmitWork = true;
var updates_num_searches = 0;
var pledges_num_searches = 0;
var workers_num_searches = 0;
var updates_sort = 'date-descending';
var pledges_sort = 'pledge-descending';
var workers_sort = 'work-ascending';

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('.table-header').click(function() {
        var cls = $(this).parent().attr('class');
        setRowToZero(cls.split('-')[0]);
        prepareToAddRows(cls, 0);
    });
    $('tbody').scroll(function() {
        var cls = $(this).attr('class');
        var table = cls.split('-')[0];
        var total = table + '-total';
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight && $(this).children().count() < total) {
            if (cls !== '') {
                var rows = addToNumRows(cls);
                prepareToAddRows(cls, rows);
            }// end if
        }// end if
    });
});

function addToNumRows(table) {
    var rows;
    if (table === 'updates') {
        updates_num_searches = updates_num_searches + 1;
        rows = updates_num_searches;
    } else if (table === 'pledges') {
        pledges_num_searches = pledges_num_searches + 1;
        rows = pledges_num_searches;
    } else if (table === 'workers') {
        workers_num_searches = workers_num_searches + 1;
        rows = workers_num_searches;
    }// end if
    return rows;
}// end addToNumRows()

function setRowToZero(table) {
    if (table === 'updates') {
        updates_num_searches = 0;
    } else if (table === 'pledges') {
        pledges_num_searches = 0;
    } else if (table === 'workers') {
        workers_num_searches = 0;
    }// end if
}// end setRowToZero()

function prepareToAddRows(cls, rows) {
    var table = cls.split('-')[0];
    var type = cls.split('-')[1];
    add_rows_to_tables(rows, table, type, setSortVariable(table, type).split('-')[1]);
}// end prepareToAddRows()

function setSortVariable(table, type) {
    var sort = null;
    if (table === 'updates') {
        if (type === updates_sort.split('-')[0]) {
            if (updates_sort.split('-')[1] === 'ascending') {
                updates_sort = type + '-descending';
            } else {
                updates_sort = type + '-ascending';
            }// end if-else
        } else {
            updates_sort = type + '-ascending';
        }// end if-else
        sort = updates_sort;
    } else if (table === 'pledges') {
        if (type === pledges_sort.split('-')[0]) {
            if (pledges_sort.split('-')[1] === 'ascending') {
                pledges_sort = type + '-descending';
            } else {
                pledges_sort = type + '-ascending';
            }// end if-else
        } else {
            pledges_sort = type + '-ascending';
        }// end if-else
        sort = pledges_sort;
    } else if (table === 'workers')  {
        if (type === workers_sort.split('-')[0]) {
            if (workers_sort.split('-')[1] === 'ascending') {
                workers_sort = type + '-descending';
            } else {
                workers_sort = type + '-ascending';
            }// end if-else
        } else {
            workers_sort = type + '-ascending';
        }// end if-else
        sort = workers_sort;
    }// end if
    return sort;
}// end setSortVariable()

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
            if (table === 'updates') {
                if (updates_num_searches == 0) $('#updates tbody').empty();
                addRowsToUpdatesTable(json);
            } else if (table === 'pledges') {
                if (pledges_num_searches == 0) $('#pledges tbody').empty();
                addRowsToPledgesTable(json);
            } else if (table === 'workers') {
                if (workers_num_searches == 0) $('#workers tbody').empty();
                addRowsToWorkersTable(json);
            }// end if
        },
    });
}// end sort()

function addRowsToUpdatesTable(json) {
    for (var index = 0; index < json.length; index++) {
        var update = json[index];
        var string = "<tr>";
        string = string + "<td class='updates-date'>" + update['date'] + "</td>";
        string = string + "<td class='updates-username'><a href='user/ " + update['username'] + "'>" + update['username'] + "</a></td>";
        string = string + "<td class='updates-description'>" + update['description'] + "</td>";
        string = string + "</tr>";
        $('#updates tbody').append(string);
    }// end for
}// end addRowsToUpdatesTable()

function addRowsToPledgesTable(json) {
    for (var index = 0; index < json.length; index++) {
        var pledge = json[index];
        var string = "<tr>";
        string = string + "<td class='pledges-username'><a href='user/ " + pledge['username'] + "'>" + pledge['username'] + "</a></td>";
        string = string + "<td class='pledges-pledged'>" + changeNumberToCurrency(pledge['pledged']) + "</td>";
        string = string + "<td class='pledges-paid'>" + changeNumberToCurrency(pledge['paid']) + "</td>";
        string = string + "</tr>";
        $('#pledges tbody').append(string);
    }// end for
}// end addRowsToPledgesTable()

function addRowsToWorkersTable(json) {
    for (var index = 0; index < json.length; index++) {
        var worker = json[index];
        var string = "<tr>";
        string = string + "<td class='workers-username'><a href='user/ " + worker['username'] + "'>" + worker['username'] + "</a></td>";
        string = string + "<td class='workers-status'>" + worker['work_status'] + "</td>";
        string = string + "<td class='workers-received'>" + changeNumberToCurrency(worker['received']) + "</td>";
        string = string + "</tr>";
        $('#workers tbody').append(string);
    }// end for
}// end addRowsToPledgesTable()

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
