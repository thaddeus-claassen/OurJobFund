var orgFirstName; 
var orgLastName;
var orgCity;
var orgState;
var orgOccupation;
var orgEducation;
var orgContact;
var orgDescription;

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    initInfoAndDescription();
    initMustConnectToString();
    $('#edit_info').click(function() {
        removeReadonlyInfoAttributes();
        $('#edit_info').css('display', 'none');
        $('#save_info').css('display', 'inline');
        $('#cancel_info').css('display', 'inline');
    });
    $('#cancel_info').click(function() {
        addReadonlyInfoAttributes();
        $('#edit_info').css('display', 'inline');
        $('#save_info').css('display', 'none');
        $('#cancel_info').css('display', 'none');
        cancelInfo();
    });
    $('#save_info').click(function() {
        $('#info_form').submit();
    });
    $('#edit_description').click(function() {
        removeReadonlyDescriptionAttributes();
        $('#edit_description').css('display', 'none');
        $('#save_description').css('display', 'inline');
        $('#cancel_description').css('display', 'inline');
    });
    $('#cancel_description').click(function() {
        addReadonlyDescriptionAttributes();
        $('#edit_description').css('display', 'inline');
        $('#save_description').css('display', 'none');
        $('#cancel_description').css('display', 'none');
        $('#id_description').text(); 
    });
    $('#save_description').click(function() {
        $('#description_form').submit();
    });
    $('#id_preferred_payment').change(function() {
        if ($(this).val() === "ANY" | $(this).val() === "CREDIT") {
            $('#must-connect-to-stripe').css('display', 'inline');
        } else {
            $('#must-connect-to-stripe').css('display', 'none');
        }// end if-else
    });
});

function initMustConnectToString() {
    if ($('#id_preferred_payment').val() === "ANY" | $('#id_preferred_payment').val() === "CREDIT") {
        $('#must-connect-to-stripe').css('display', 'inline');
    } else {
        $('#must-connect-to-stripe').css('display', 'none');
    }// end if-else
}// end initMustConnectToString()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function initInfoAndDescription() {
    orgFirstName = $('#id_first_name').val();
    orgLastName = $('#id_last_name').val();
    orgCity = $('#id_city').val();
    orgState = $('#id_state').val();
    orgOccupation = $('#id_occupation').val();
    orgEducation = $('#id_education').val();
    orgContact = $('#id_contact').val();
    orgDescription = $('#id_description').val();
    addReadonlyInfoAttributes();
    addReadonlyDescriptionAttributes();
}// end initInfoAndDescription()

function cancelInfo() {
    $('#id_first_name').val(orgFirstName);
    $('#id_last_name').val(orgLastName);
    $('#id_city').val(orgCity);
    $('#id_state').val(orgState);
    $('#id_occupation').val(orgOccupation);
    $('#id_education').val(orgEducation);
    $('#id_contact').val(orgContact);
}// end cancelInfo()

function cancelDescription() {
    $('#id_description').val(orgDescription);
}// end cancelDescription()

function removeReadonlyInfoAttributes() {
    $('.info').each(function(index) {
        if ($(this).attr('type') === 'text') {
            $(this).removeAttr('readonly');
        } else {
            $(this).removeAttr('disabled');
        }// end if-else
    });
}// end removeReadOnlyAttributes()

function addReadonlyInfoAttributes() {
    $('.info').each(function(index) {
        if ($(this).attr('type') === 'text') {
            $(this).prop('readonly', true);
        } else {
            $(this).prop('disabled', true);
        }// end if-else
    });
}// end addReadonlyInfoAttributes()

function removeReadonlyDescriptionAttributes() {
    $('#id_description').removeAttr('readonly');
}// end removeReadOnlyDescriptionAttributes()

function addReadonlyDescriptionAttributes() {
    $('#id_description').prop('readonly', true);
}// end addReadonlyDescriptionAttributes()

function mustConnectToStripe() {
    $('#must-connect-to-stripe')
}// end mustConnectToStripe()