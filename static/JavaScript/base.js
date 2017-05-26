
$('document').ready(function() {

});

function viewNotification(notification_id) {
    var id = notification_id.substr(20, notification_id.length);
    document.location = '/jobuser/view_notification/' + id.toString(); 
}// end viewPledgeNotification()
















