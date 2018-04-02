var canSubmitPledge = true;
var canSubmitWork = true;
var updates_num_searches = 0;
var pledges_num_searches = 0;
var workers_num_searches = 0;
var updates_sort = 'date-descending';
var pledging_sort = 'pledge-descending';
var working_sort = 'work-ascending';

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
    } else if (table === 'pledging') {
        pledging_num_searches = pledging_num_searches + 1;
        rows = pledging_num_searches;
    } else if (table === 'working') {
        working_num_searches = working_num_searches + 1;
        rows = working_num_searches;
    }// end if
    return rows;
}// end addToNumRows()

function setRowToZero(table) {
    if (table === 'updates') {
        updates_num_searches = 0;
    } else if (table === 'pledging') {
        pledging_num_searches = 0;
    } else if (table === 'working') {
        working_num_searches = 0;
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
    } else if (table === 'pledging') {
        if (type === pledging_sort.split('-')[0]) {
            if (pledging_sort.split('-')[1] === 'ascending') {
                pledging_sort = type + '-descending';
            } else {
                pledging_sort = type + '-ascending';
            }// end if-else
        } else {
            pledging_sort = type + '-ascending';
        }// end if-else
        sort = pledging_sort;
    } else if (table === 'workers')  {
        if (type === working_sort.split('-')[0]) {
            if (working_sort.split('-')[1] === 'ascending') {
                working_sort = type + '-descending';
            } else {
                working_sort = type + '-ascending';
            }// end if-else
        } else {
            working_sort = type + '-ascending';
        }// end if-else
        sort = working_sort;
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
            } else if (table === 'pledging') {
                if (pledging_num_searches == 0) $('#pledging tbody').empty();
                addRowsToPledgingTable(json);
            } else if (table === 'working') {
                if (working_num_searches == 0) $('#working tbody').empty();
                addRowsToWorkingTable(json);
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

function addRowsToPledgingTable(json) {
    for (var index = 0; index < json.length; index++) {
        var pledge = json[index];
        var string = "<tr>";
        string = string + "<td class='pledging-username'><a href='user/ " + pledge['username'] + "'>" + pledge['username'] + "</a></td>";
        string = string + "<td class='pledging-pledged'>" + changeNumberToCurrency(pledge['pledging']) + "</td>";
        string = string + "<td class='pledging-paid'>" + changeNumberToCurrency(pledge['paid']) + "</td>";
        string = string + "</tr>";
        $('#pledging tbody').append(string);
    }// end for
}// end addRowsToPledgesTable()

function addRowsToWorkingTable(json) {
    for (var index = 0; index < json.length; index++) {
        var worker = json[index];
        var string = "<tr>";
        string = string + "<td class='working-username'><a href='user/ " + worker['username'] + "'>" + worker['username'] + "</a></td>";
        string = string + "<td class='working-status'>" + worker['work_status'] + "</td>";
        string = string + "<td class='working-received'>" + changeNumberToCurrency(worker['received']) + "</td>";
        string = string + "<td class='working-payment'>";
        if (worker['username'] === $('#username').val()) {
            if ($('#unconfirmed_payments').val() != '') {
                string = string + "<a href='#'>Unconfirmed Payment/s</a></td>";
            }// end if
        } else {
            string = string + "<a href='pay/" + $('#random_string').val() + "/" + worker['username'] + "'>Make Payment</a></td>";
        }// end if-else
        string = string + "</tr>";
        $('#working tbody').append(string);
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
