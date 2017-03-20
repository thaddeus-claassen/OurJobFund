var usernameIsValid = false;
var passIsValid = false;
var passwordsMatch = false;
var atLeastThirteen = false;
var attemptedToCreateUserButError = false;
$('document').ready(function() {
    $('#create-user-form').submit(function(event) {
        if (usernameIsValid && passwordIsValid && passwordsMatch && atLeastThirteen) {
            
        } else {
            errorMessages();
            attemptedToCreateUserButError = true;
            event.preventDefault();
        }// end if-else
    });
    $('#id_username').after('<span id="id_username_span"></span>');
    $('#id_username').keyup(function() {
        if ($('#id_username').val().length > 0) {
            verifyUsername();
        }// end if
    });
    $('#id_password').after('<span id="id_password_span"></span>');
    $('#id_repeat_password').after('<span id="id_repeat_password_span"></span>');
    $('#id_password').keyup(function() {
        passIsValid = verifyPassword();
        if ($(this).val() > 0 && $('#id_repeat_password').val() > 0) {
            passwordsMatch = verifySamePassword();
        }// end if
    });
    $('#id_repeat_password').keyup(function() {
        if ($(this).val().length > 0 && $('#id_password').val().length > 0) {
            passwordsMatch = verifySamePassword();
        }// end if
    });
    $('#is-at-least-thirteen').change(function() {
        atLeastThirteen = $(this).is(':checked'); 
        if (attemptedToCreateUserButError) {
            if (atLeastThirteen) {
                deleteCheckboxErrorMessage();
            } else {
                createCheckboxErrorMessage();
            }// end if-else
        }// end if
    });
});

function verifyUsername() {
    $.ajax({
        type : 'GET',
        url : 'verify_username',
        data : {
            'username' : $('#id_username').val(),
        },
        error : usernameFailure,
        success : usernameSuccess,
    });
}// end verifyUsername()

function usernameFailure() {
    usernameIsValid = false;
}// end usernameFailure()

function usernameSuccess(usernameExists) {
    usernameIsValid = true;
    if (usernameExists === 'true') {
        $('#id_username_span').text('&nbsp; Username is already used');
    } else {
        $('#id_username_span').text('&nbsp; Username is valid');
    }// end if-else
}// end usernameSuccess()

function verifyPassword() {
    var verifyPass = passwordIsValid();
    passValidText(verifyPass);
    return verifyPass;
}// end verifyPassword()

function passwordIsValid() {
    var isValid = false;
    var pass = $('#id_password').val();
    if (pass.length >= 9) {
        if (hasLowercase(pass)) {
            if (hasUppercase(pass)) {
                if (hasNumeric(pass)) {
                    isValid = true;
                }// end if
            }// end if
        }// end if
    }// end if
    return isValid;
}// end passwordIsValid()

function passValidText(isValid) {
    if (isValid) {
        $('#id_password_span').text('&nbsp;Password is valid');
        $('#id_password_span').css('color','green');
    } else {
        $('#id_password_span').text('&nbsp;Password is not valid');
        $('#id_password_span').css('color','red');
    }// end if-else
}// end passValidText

function hasLowercase(string) {
    var hasLowercase = false;
    for(x = 0; x < string.length ; x++) {
        if(string.charAt(x) >= 'a' && string.charAt(x) <= 'z') {
            hasLowercase = true;
        }// end if
    }// end for
    return hasLowercase;
}// end has hasLowercase()

function hasUppercase(string) {
    var hasUppercase = false;
    for(x = 0; x < string.length ; x++) {
        if(string.charAt(x) >= 'A' && string.charAt(x) <= 'Z') {
            hasUppercase = true;
        }// end if
    }// end for
    return hasUppercase;
}// end has upperCase()

function hasNumeric(string) {
    var hasNumeric = false;
    for(x = 0; x < string.length ; x++) {
        if(string.charAt(x) >= '0' && string.charAt(x) <= '9') {
            hasNumeric = true;
        }// end if
    }// end for
    return hasNumeric;
}// end hasNumeric()

function verifySamePassword() {
    var passesMatch = ($('#id_password').val() === $('#id_repeat_password').val());
    if (passesMatch) {
        $('#id_repeat_password_span').text('Passwords match');
        $('#id_repeat_password_span').css('color', 'green');
    } else {
        $('#id_repeat_password_span').text('Passwords do not match');
        $('#id_repeat_password_span').css('color', 'red');
    }// end if-else
    return passesMatch;
}// end verifySamePassword()

function deleteCheckboxErrorMessage() {
    $('#is-at-least-thirteen-span').css('display', 'none');
}// end deleteCheckboxErrorMessage()

function createCheckboxErrorMessage() {
    $('#is-at-least-thirteen-span').text('You must click this checkbox to continue onto the website');
    $('#is-at-least-thirteen-span').css('color', 'red');
}// end createCheckboxErrorMessage()

function errorMessages() {
    if (!atLeastThirteen) {
        createCheckboxErrorMessage();
    }// end if
}// end errorMessages()























