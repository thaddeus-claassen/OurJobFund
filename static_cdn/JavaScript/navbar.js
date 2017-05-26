var messagesJson;

$('document').ready(function() {
    $('#user_search_bar').keydown(function(event) {
        if (event.which == 13) {
            go_to_users_page();
        } else {
            search_users();
        }// end if-else
    });
});

function search_users() {
    $.ajax({
        url : "search_users",
        data : {
            'search' : $('#user_search_bar').val(),
        },
        success : userSearchSuccess,
    });
}// end search_users()

function userSearchSuccess(json) {
    $('#users').empty();
    var numUsers = Object.keys(json).length; 
    if (numUsers > 0) {
        for (var index = 0; index < json.length; index++) {
            if (index < 5) {
                var user = json[index];
                var fields = user["fields"];
                $('#users').append("<option value='" + fields["first_name"] + " " + fields["last_name"] + "'>");
            } else {
                $('#users').append("<option value='" + View All + "' onclick='viewUsers()' >");
            }// end if-else
        }// end for
    }// end if
}// end userSearchSuccess()

function viewUsers() {
    userSearch = $('#user_search_bar').replace(/\s/g, '.');
    document.location.href = '/user/view_users/' + userSearch;
}// end viewUsers()

function viewNotification(notification_id) {
    var id = notification_id.substr(20, notification_id.length);
    document.location = '/jobuser/view_notification/' + id.toString(); 
}// end viewPledgeNotification()
















