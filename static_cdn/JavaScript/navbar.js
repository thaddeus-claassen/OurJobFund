$('document').ready(function() {
    $('#user_search_bar').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            search_users();
        }// end if
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
    alert(string);
    if (string === "user exists") {
        $('#go_to_user').attr('action', "user/" + $('#user_search_bar').val());        
        $('#go_to_user').submit();
    }// end if
}// end userSearchSuccess()