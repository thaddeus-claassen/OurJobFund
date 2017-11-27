$('document').ready(function() {
    $('#username').click(function() {
        changeUsername();
    });
    $('#cancel-username').click(function() {
        cancelUsername();
    });
    $('#email').click(function() {
        changeEmail();
    });
    $('#cancel-email').click(function() {
        cancelEmail();
    });
    $('#password').click(function() {
        changePassword();
    });
    $('#cancel-password').click(function() {
        cancelPassword();
    });
    $('#delete-account').click(function() {
        deleteAccount();
    });
    $('#cancel-delete-account').click(function() {
        cancelDeleteAccount();
    });
});

function changeUsername() {
    $('#current-username').css('display', 'none');
    $('#change-username').css('display', 'block');
}// end changeName()

function cancelUsername() {
    $('#current-username').css('display', 'block');
    $('#change-username').css('display', 'none');
}// end cancelName()

function changeEmail() {
    $('#current-email').css('display', 'none');
    $('#change-email').css('display', 'block');
}// end changeEmail()

function cancelEmail() {
    $('#current-email').css('display', 'block');
    $('#change-email').css('display', 'none');
}// end cancelEmail()

function changePassword() {
    $('#current-password').css('display', 'none');
    $('#change-password').css('display', 'block');
}// end changePassword()

function cancelPassword() {
    $('#current-password').css('display', 'block');
    $('#change-password').css('display', 'none');
}// end cancelPassword()

function deleteAccount() {
    $('#delete-account').css('display', 'none');
    $('#delete-account-clicked').css('display', 'block');
}// end deleteAccount()

function cancelDeleteAccount() {
    $('#delete-account').css('display', 'block');
    $('#delete-account-clicked').css('display', 'none');
}// end cancelDeleteAccount()
