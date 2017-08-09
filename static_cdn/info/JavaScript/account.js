$('document').ready(function() {
    $('#name').click(function() {
        changeName();
    });
    $('#cancel-name').click(function() {
        cancelName();
    });
    $('#email').click(function() {
        changeEmail();
    });
    $('#cancel-email').click(function() {
        alert('Cancel email clicked')
        cancelEmail();
        alert('Hello?');
        alert($('#current-email').css('display'));
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

function changeName() {
    $('#current-name').css('display', 'none');
    $('#change-name').css('display', 'block');
}// end changeName()

function cancelName() {
    $('#current-name').css('display', 'block');
    $('#change-name').css('display', 'none');
}// end cancelName()

function changeEmail() {
    $('#current-email').css('display', 'none');
    $('#change-name').css('display', 'block');
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
    $('#current-delete-account').css('display', 'block');
    $('#change-delete-account').css('display', 'none');
}// end cancelDeleteAccount()
