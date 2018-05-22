var canSubmit = true;

$('document').ready(function() {
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }// end if
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('#go_to_user').submit(function(event) {
        if (canSubmit) {    
            canSubmit = false;
            username = $('#user_search_bar').val(); 
            if (username === "") {
                canSubmit = true;
                event.preventDefault();
            } else {
                check_if_user_exists(username);
            }// end if-else
        } else {
            event.preventDefault()
        }// end if-else
    });
});

function check_if_user_exists(username) {
    $.ajax({
        url : 'search-user',
        data : {
            'username' : username,
        },
        success: function(json) {
            if (json !== "") location = '/' + json['username'];
        },
    });
}// end check_if_user_exists()

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