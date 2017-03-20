$('document').ready(function() {
    get_user_info();
    $('#add_dependent').click(function() {
        $('#add_dependent_modal').css('display', 'inline');
    });
    $('#add_dependent_user').click(function() {
        if (usernameIsValid && passIsValid && passwordsMatch && atLeastThirteen) {
            add_dependent();
            $('#add_dependent_modal').css('display', 'none');
        } else {
            errorMessages();
            attemptedToCreateUserButError = true;
        }// end if-else
    });
    $('#message_button').click(function() {
        createMessage();
    });
    $('#send_modal_message').click(function() {
        send_message();
        $('#message').val('');
        $('#message_modal').css('display', 'none');
    });
    $('.close_modal').click(function() {
        $('.modal').css('display', 'none');
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

function add_dependent() {
    $.ajax({
        type : "POST",
        url : "add_dependent",
        data : {
            'username' : $('#id_username').val(),
            'password' : $('#id_password').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
    });
}// end addDependent()

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

function get_user_info() {
    $.ajax({
        url : "get_user_info",
        data : {
            'user_id' : $('#user_id').val(),
        },
        success : applyUserInfo,
    });
}// end userInfo()

function applyUserInfo(json) {
    if (json['first_name'] != "") {
        $('#first_name').text(json['first_name']);
    } else {
        $('#first_name').text("First name not specified");
    }// end if-else
    if (json['last_name'] != "") {
        $('#last_name').text(json['last_name']);    
    } else {
        $('#last_name').text("Last name not specified");
    }// end if-else
    if (json['city'] != "") {
        $('#city').text(json['city']);
    } else {
        $('#city').text("City not specified");
    }// end if-else
    if (json['state'] != "") {
        $('#state').text(json['state']);
    } else {
        $('#state').text("State not specified");
    }// end if-else     
    $('#description').text(json['description']);
}// end applyUserInfo()



