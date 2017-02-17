$('document').ready(function() {
    $('#message_button').click(function() {
        createMessage();
    });
    $('#send_modal_message').click(function() {
        send_message();
        $('#message').val('');
        $('#message_modal').css('display', 'none');
    });
    $('#close_modal').click(function() {
        $('#message_modal').css('display', 'none');
    });
    $('#make_edits').click(function() {
        makeEdits();
    });
    $('#edit_description').click(function() {
        $('#edit_description').css('display', 'none')
        $('#description').css('display', 'none');
        $('#textarea_description').css('display', 'inline');
        $('#save_description').css('display', 'inline');
    });
    $('#save_description').click(function() {
        save_description();
        $('#description').text($('#textarea_description').val());
        $('#textarea_description').css('display', 'none');
        $('#description').css('display', 'inline');
        $('#save_description').css('display', 'none');
        $('#edit_description').css('display', 'inline');
    });
    $('[name=public_pledge_filter]').change(function() {
        change_public_pledge_filter();
    });
    $('[name=public_worker_filter]').change(function() {
        change_public_worker_filter();
    });
    $('#use_pledge_filter').click(function() {
        copy_pledge_filter();
    });
    $('#user_worker_filter').click(function() {
        copy_worker_filter();
    });
});

function makeAllInformationPublic() {
 
}// end makeAllInformationPublic()

function save_description() {
    $.ajax({
        type : "POST",
        url : "save_description",
        data : {
            'description' : $('#textarea_description').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end save_description()

function createMessage() {
    $('#message_modal').css('display', 'inline');
}// end createModal()

function send_message() {
    $.ajax({
        type : "POST",
        url : "send_message",
        data : {
            'receiver' : $('#username').text(),
            'message' : $('#message').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end send_message()

function makeEdits() {
    $('#make_edits_button_div').css('display', 'none');
    $('#edit_div').css('display', 'inline');
}// end makeEdits()

function change_public_pledge_filter() {
    $.ajax({
        type : "POST",
        url : "change_public_pledge_filter",
        data : {
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// ed change_public_pledge_filter()

function change_public_worker_filter() {
    $.ajax({
        type : "POST",
        url : "change_public_worker_filter",
        data : {
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// ed change_public_worker_filter()

function copy_pledge_filter() {
    $.ajax({
        type : "POST",
        url : "copy_pledge_filter",
        data : {
            'user_id' : $('#user_id').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end copy_pledge_filter()

function copy_worker_filter() {
    $.ajax({
        type : "POST",
        url : "copy_worker_filter",
        data : {
            'user_id' : $('#user_id').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end copy_worker_filter()




