var canSubmit = true;

$('document').ready(function() {
    $('#sign-up-form').submit(function(e) {
        if (canSubmit) {
            canSubmit = false;
        } else {
            e.preventDefault();
        }// end if-else
    });
});

function createSpansAboveInputsForErrorMessages() {
    $('#id_first_name').before("<div class='row'><div class='col-md-12'><span id='id_first_name_span'></span></div></div>'");
    $('#id_last_name').before("<div class='row'><div class='col-md-12'><span id='id_last_name_span'></span></div></div>'");
    $('#id_email').before("<div class='row'><div class='col-md-12'><span id='id_email_span'></span></div></div>'");
    $('#id_password').before("<div class='row'><div class='col-md-12'><span id='id_password_span'></span></div></div>'");
    $('#id_repeat_password').before("<div class='row'><div class='col-md-12'><span id='id_repeat_password_span'></span></div></div>'");
}// end createSpansAfterInputsForErrorMessages()

function emailFailure() {
    usernameIsValid = false;
}// end usernameFailure()

function emailSuccess(emailExists) {
    emailIsValid = true;
    if (emailExists) {
        $('#id_username_span').text('email is already in use');
    }// end if
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























