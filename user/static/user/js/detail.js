$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    disableInfo();
    $(document).on('input', 'input:text', function() {
        save_input($(this));
    });
    $(document).on('input', 'textarea', function() {
        save_input($(this));
    });
    $('select').change(function() {
        save_input($(this));
    });
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function disableInfo() {
    if ($('#this_user').val() !== $('#username').text()) {
        $('#id_first_name').attr('readonly', true);
        $('#id_last_name').attr('readonly', true);
        $('#id_city').attr('readonly', true);
        $('#id_state').attr('disabled', true);
        $('#id_education').attr('readonly', true);
        $('#id_occupation').attr('readonly', true);
        $('#id_contact').attr('readonly', true);
        $('#id_description').attr('readonly', true);
    }// end if
}// end disableInfo()

function sort(sort) {
    ascending_or_descending = 'ascending';
    if (sort === currSort.split('-')[0] && currSort.split('-')[1] === 'ascending') {
        ascending_or_descending = 'descending';
    }// end if
    currSort = sort + "-" + ascending_or_descending;
    $.ajax({
        url : $(location).attr('href') + "sort",
        data : {
            'sort' : sort,
            'ascending_or_descending' : ascending_or_descending,
        },
        success: sortSuccess,
    });
}// end sort()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function save_input(input) {
    $.ajax({
        url : 'save_input',
        type: 'POST',
        data : {
            'id' : $(input).attr('id'),
            'value' : $(input).val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
    });
}// end save_input()