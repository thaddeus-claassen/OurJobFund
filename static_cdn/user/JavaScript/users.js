var numSearches = 1;

$('document').ready(function() {
    $(window).scroll(function(){
        if ($(window).scrollTop() == $(document).height()-$(window).height()) {
            if (50 * numSearches < parseInt($('#total').val())) {
                see_more_users();
            }// end if
        }// end if
    });
});

function see_more_users() {         
    $.ajax({
        url : 'see_more_users',
        data : {
            'numSearches' : numSearches,
            'search' : $('#query').val(),
        },
        success: seeMoreUsersSuccess,
    });
}// end see_more_users()

function seeMoreUsersSuccess(json) {
    numSearches = numSearches + 1;
    var numUsers = Object.keys(json).length; 
    if (numUsers > 0) {
        for (var index = 0; index < json.length; index++) {
            var user = json[index];
            var fields = job["fields"];
            $('#user-table').append("<tr><td><a href='" + fields["random_string"] + "'> " + fields["first_name"] + " " + fields["last_name"] + "</a></td></tr>");
        }// end for
    }// end if
}// end seeMoreUsersSuccess()