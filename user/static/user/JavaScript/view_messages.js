$('document').ready(function() {
    get_messages();
    $('#send_message').click(function() {
        send_message();
    });
    $('#send_message_textarea').keydown(function(event) {
        if (event.which == 13) {
            send_message();
        }// end if 
    });
});

function get_messages() {
    $.ajax({
        type : 'POST',
        url : "get_messages",
        data : {
            'other_user' : $('#other_user').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : applyMessages,
    });
}// end get_messages()

function send_message() {
    $.ajax({
        type : "POST",
        url : "send_message",
        data : {
            'receiver' : $('#other_user').val(),
            'message' : $('#send_message_textarea').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : applyMessage
    });
}// end send_message()

function applyMessages(json) {
    if (json.length > 0) {
        for (var index = 0; index < json.length; index++) {
            var fields = json[index]['fields'];
            var string = "";
            string += "<div class='row'>";
            string += "    <div class='col-md-12'>From: " + fields['sender'] + "</div>";
            string += "</div>";
            string += "<div class='row'>";
            string += "    <div class='col-md-12'>To: " + fields['receiver'] + "</div>";
            string += "</div>";
            string += "<div class='row'>";         
            string += "    <div class='col-md-12'>" + fields['message'] + "</div>";
            string += "</div>";
            string += "<div class='row'>";         
            string += "    <div class='col-md-12'>Sent: " + fields['date_sent'] + "</div>";
            string += "<div>";
            $('#message_container').prepend(string);
        }// end for
    }// end if
}// end applyMessages()

function applyMessage() {
    var message = $('#send_message_textarea').val();
    var string = "";
    string += "<div class='row'>";
    string += "    <div class='col-md-12'>From: " + $('#user').val() + "</div>";
    string += "</div>";
    string += "<div class='row'>";
    string += "    <div class='col-md-12'>To: " + $('#other_user').val() + "</div>";
    string += "</div>";
    string += "<div class='row'>";
    string += "    <div class='col-md-12'>" + message + "</div>";
    string += "</div>";
    string += "<div class='row'>";
    string += "    <div class='col-md-12'>Send: " + new Date() + "</div>";
    string += "</div>";
    $('#textarea_row').before(string);
    $('#send_message_textarea').val("");
}// end applyMessage()

