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
});

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
    $('#id_first_name').removeAttr('readonly');
    $('#id_last_name').removeAttr('readonly');
    $('#id_city').removeAttr('readonly');
    $('#id_state').removeAttr('disabled');
    $('#id_education').removeAttr('readonly');
    $('#id_occupation').removeAttr('readonly');
    $('#id_contact').removeAttr('readonly');
}// end removeReadOnlyAttributes()

function addReadonlyInfoAttributes() {
    $('#inputId').prop('readonly', false);
    $('#id_first_name').prop('readonly', false);
    $('#id_last_name').prop('readonly', false);
    $('#id_city').prop('readonly', false);
    $('#id_state').prop('disabled', false);
    $('#id_education').prop('readonly', false);
    $('#id_occupation').prop('readonly', false);
    $('#id_contact').prop('readonly', false);
}// end addReadonlyInfoAttributes()

function removeReadonlyDescriptionAttributes() {
    $('#id_description').removeAttr('readonly');
}// end removeReadOnlyDescriptionAttributes()

function addReadonlyDescriptionAttributes() {
    $('#id_description').prop('readonly', false);
}// end addReadonlyDescriptionAttributes()