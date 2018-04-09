var canSubmit = true;

$('document').ready(function() {
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }// end if
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
            'username' : username
        },
        success: function(json) {
            if (json !== "") location = '/' + json['username'];
        },
    });
}// end check_if_user_exists()