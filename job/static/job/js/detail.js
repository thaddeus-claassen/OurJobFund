var canSubmitPledge = true;
var canSubmitWork = true;
var update_sort = 'date-descending';
var pledge_sort = 'pledge-descending';
var work_sort = 'status-ascending';

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('.sort').click(function() {
        var id = $(this).attr('id');
        setSortVariable(id);
        sortTable(id);
    });
});

function setSortVariable(id) {
    var table = id.split('-')[0];
    var type = id.split('-')[1];
    if (table === 'updates') {
        if (type === update_sort.split('-')[0]) {
            if (update_sort.split('-')[1] === 'ascending') {
                update_sort = type + '-descending';
            } else {
                update_sort = type + '-ascending';
            }// end if-else
        } else {
            update_sort = type + '-ascending';
        }// end if-else
    } else if (table === 'pledges') {
        if (type === pledge_sort.split('-')[0]) {
            if (pledge_sort.split('-')[1] === 'ascending') {
                pledge_sort = type + '-descending';
            } else {
                pledge_sort = type + '-ascending';
            }// end if-else
        } else {
            pledge_sort = type + '-ascending';
        }// end if-else
    } else if (table === 'work')  {
        if (type === work_sort.split('-')[0]) {
            if (work_sort.split('-')[1] === 'ascending') {
                work_sort = type + '-descending';
            } else {
                work_sort = type + '-ascending';
            }// end if-else
        } else {
            work_sort = type + '-ascending';
        }// end if-else
    }// end if
}// end setSortVariable()

function sortTable(id) {
    var table, variable, col, ascending_or_descending, sortType;
    if (id.split('-')[0] === 'updates') {
        table = document.getElementById('updates');
        variable = update_sort;
    } else if (id.split('-')[0] === 'pledges') {
        table = $('#pledges');
        variable = pledge_sort;
    } else if (id.split('-')[0] === 'workers') {
        table = $('#workers');
        variable = workers_sort;
    }// end if
    if (variable.split('-')[1] === 'ascending') ascending_or_descending = 'ascending';
    else ascending_or_descending = 'descending';
    if (variable.split('-')[0] === 'username' || variable.split('-')[0] === 'status' || variable.split('-')[0] === 'title') {
        if (variable.split('-')[0] === 'username') col = 0;
        else if (variable.split('-')[0] === 'status') col = 1;
        else col = 2;
        sortStrings(table, col, ascending_or_descending);
    } else if (variable.split('-')[0] === 'pledged' || variable.split('-')[0] === 'paid' || variable.split('-')[0] === 'requesting' || variable.split('-')[0] === 'received') {
        if (variable.split('-')[0] === 'pledged') col = 1;
        else if (variable.split('-')[0] === 'paid' || variable.split('-')[0] === 'requesting') col = 2;
        else col = 3;
        sortNumbers(table, col, ascending_or_descending);
    } else if (variable.split('-')[0] === 'date') {
        sortDates(table, 1, ascending_or_descending);
    }// end if
}// end sortTable

function sortStrings(table, col, ascending_or_descending) {
    if (ascending_or_descending === 'ascending') {
        var rows, shouldSwitch, i;
        var switching = true;
        while (switching) {
            switching = false;
            rows = table.getElementsByTagName('TR');
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                var x = rows[i].getElementsByTagName("TD")[col];
                var y = rows[i + 1].getElementsByTagName("TD")[col];
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }// end if
            }// end for
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }// end if
        }// end while
    } else {
        reverseRows(table);
    }// end if-else
}// end sortStrings()

function sortNumbers(table, col, ascending_or_descending) {
    if (ascending_or_descending === 'ascending') {
        var rows, shouldSwitch, i;
        var switching = true;
        while (switching) {
            switching = false;
            rows = table.getElementsByTagName('TR');
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                var x = rows[i].getElementsByTagName("TD")[col];
                var y = rows[i + 1].getElementsByTagName("TD")[col];
                if (Number(x.innerHTML) > Number(y.innerHTML)) {
                    shouldSwitch= true;
                    break;
                }// end if
            }// end for
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }// end if
        }// end while
    } else {
        reverseRows(table)
    }// end if-else
}// end sortNumbers()

function sortDates(table, col, ascending_or_descending) {
    if (ascending_or_descending === 'descending') {
        var rows, shouldSwitch, i;
        var switching = true;
        while (switching) {
            switching = false;
            rows = table.getElementsByTagName('TR');
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                var x = rows[i].getElementsByTagName("TD")[col];
                var y = rows[i + 1].getElementsByTagName("TD")[col];
                var dateX = Date($(x).attr('class'));
                var dateY = Date($(y).attr('class'));
                if (dateX < dateY) {
                    shouldSwitch= true;
                    break;
                }// end if
            }// end for
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }// end if
        }// end while
    } else {
        reverseRows(table);
    }// end if-else
}// end sortDates()

function reverseRows(table) {
    var rows = [];
    $(table).find('tr').each(function(i, e) {
        if (i > 0) {
            rows[i] = e;
        }// end if
    });
    rows = rows.reverse();
    $(table).find('tbody').empty();
    for (r in rows) {
        $(table).find('tbody').append("<tr>" + rows[r].innerHTML + "</tr>");
    }// end for
}// end reverseRows()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()
