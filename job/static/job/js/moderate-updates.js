var canSubmit = true;
var num_searches = 0;
var sort = 'date-descending';

$('document').ready(function() {
    $('form').submit(function(event) {
        if (canSubmit) {
            canSubmit = false;
        } else {
            event.preventDefault();
        }// end if-else
    });
    $('.table-header').click(function() {
        var cls = $(this).parent().attr('class');
        num_searches = 0;
        setSort(cls);
            
    });
    $('tbody').scroll(function() {
        var cls = $(this).parent().attr('class');
        var table = cls.split('-')[0];
        var total = table + '-total';
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight && $(this).children().count() < total) {
            if (cls !== '') {
                num_searches = num_searches + 1;
                
            }// end if
        }// end if
    });
});

function setSort(cls) {
    if (sort.split('-')[0] === cls) {
        if (sort.split('-')[1] === 'ascending') {
            sort = cls + '-descending';
        } else {
            sort = cls + '-ascending';
        }
    } else {
        sort = cls + 'ascending';
    }// end if-else
}// end setSort()

function add_rows_to_tables() {
    $.ajax({
        url : 'sort',
        data : {
            'num_searches' : num_searches,
            'table' : 'updates',
            'column' : sort.split('-')[0],
            'order' : sort.split('-')[1],
        },
        success: addRowsToTable(),
    });
}// end sort()

function addRowsToTable(json) {
    if (num_searches == 0) $('#updates tbody').empty();
    for (var index = 0; index < json.length; index++) {
        var update = json[index];
        var img = update['images'];
        if (img > 0) img = "<a href='update/" + update['random_string'] + "/images'>" + update['images'] + "</a>";
        else img = 0;
        var string = "<tr>";
        string = string + "<td class='username'><a href='user/ " + update['username'] + "'>" + update['username'] + "</a></td>";
        string = string + "<td class='date'>" + update['date'] + "</td>";
        string = string + "<td class='images'>" + img + "</td>";
        string = string + "<td class='delete'><input type='submit' value='Delete' name='" + update['random_string'] + "'/></td>";
        string = string + "</tr>";
        string = string + "<tr>";
        string = string + "<td class='updates-comment' colspan='3'>" + update['comment'] + "</td>";
        string = string + "</tr>";
        $('tbody').append(string);
    }// end for
}// end addRowsToTable()