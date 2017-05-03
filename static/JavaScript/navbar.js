var messagesJson;

$('document').ready(function() {
    $('#user_search_bar').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            search_users();
        }// end if
    });
    $('.close_modal').click(function() {
        $('#view_message_modal').css('display', 'none');
    });
});

function search_users() {
    $.ajax({
        type : "GET",
        url : "search_users",
        data : {
            'username' : $('#user_search_bar').val(),
        },
        success : userSearchSuccess,
    });
}// end search_users()

function userSearchSuccess(string) {
    if (string === "user exists") {
        var firstAction = $('#go_to_user').attr('action');
        var newAction = firstAction.substring(0, firstAction.length - 1) + $('#user_search_bar').val();
        $('#go_to_user').attr('action', newAction);
        $('#go_to_user').submit();
    }// end if
}// end userSearchSuccess()

function viewPledgeNotification(notification_id) {
    var id = notification_id.substr(20, notification_id.length);
    document.location = '/jobuser/view_pledge_notification/' + id.toString(); 
}// end viewPledgeNotification()

function viewWorkNotification(notification_id) {
    var id = notification_id.substr(18, notification_id.length);
    document.location = '/jobuser/view_work_notification/' + id.toString(); 
}// end viewWorkNotification()
















