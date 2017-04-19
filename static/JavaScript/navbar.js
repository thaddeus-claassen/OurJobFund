var messagesJson;

$('document').ready(function() {
    get_num_unviewed_messages();
    $('#open_messages_dropdown').click(function() {
        get_messages_for_navbar();
    });
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

function get_num_unviewed_messages() {
    $.ajax({
        url : 'get_num_unviewed_messages',
        success : applyMessageNumber,
    });
}// end get_num_unviewed_messages()

function applyMessageNumber(numMessages) {
    
}// end applyMessageNumber()

function get_messages_for_navbar() {
    $.ajax({
        url : 'get_messages_for_navbar',
        success : applyNavbarMessages,
    });
}// end get_messages()

function applyNavbarMessages(json) {
    messagesJson = json;
    $('#add_messages').empty();
    var user = $('#user').val();                        
    if (messagesJson.length > 0) {
        for (var index = 0; index < messagesJson.length; index++) {
            var fields = messagesJson[index]['fields'];
            var otherUser;
            if (fields['sender'] == user) {
                otherUser = fields['receiver'];
            } else {
                otherUser = fields['sender'];
            }// end if-else
            $('#add_messages').append("<li id='" + fields['sender'] + '-' + fields['receiver'] + '-' + messagesJson[index]['pk'] + "' onclick='makeMessageModal(this.id)'><a href='#'>" + otherUser + " " + fields['message'].substring(0,20) + "</a></li>");
        }// end for
    }// end if
}// end applyNavbarMessages()

function makeMessageModal(messageID) {
    var message;
    for (var index = 0; index < messagesJson.length; index++) {
        message = messagesJson[index];
        var pk = message['pk'];
        var ID;
        for (var i = messageID.length - 1; i >= 0; i--) {
            var charMessageID = messageID[i];
            if (charMessageID == '-') {
                ID = messageID.substring(i + 1, messageID.length);
                break;
            }// end if
        }// end for
        if (ID == pk) {
            break;
        }// end if
    }// end for
    $('#message_date_sent').text(message['fields']['date_sent']);
    $('#message_sender').text(message['fields']['sender']);
    $('#message_receiver').text(message['fields']['receiver']);
    $('#message_message').text(message['fields']['message']);
    $('#view_message_modal').css('display', 'inline');
}// end makeMessageModal()

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
















