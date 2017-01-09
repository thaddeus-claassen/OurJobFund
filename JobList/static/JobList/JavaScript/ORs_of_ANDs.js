function getURL() {
    return "get_ORs_of_ANDs_tags";
}// end getURL()

function applyMetric() {
    var string = getHashtagsString();
    save_tags(string);
}// end applyMetric()

function addOuterSpan(numCols) {
    if (numCols > 0) {
        $('#group' + numCols).after('<span id="group' + numCols + 'span" class="outside_clause">OR</span>');
    }// end if
}// end addOuterSpan()

function addInnerSpan(groupID, rowNumber) {
    $('#' + groupID).append('<tr id="' + groupID + "row" + (rowNumber - 1) + 'span"><td><span class="inside_clause" style="display: inline;">AND</span></td></tr>');
}// end addInnerSpan()

function innerLogic() {
    return '&';
}// end innerLogic()

function outerLogic() {
    return '|';
}// end outerLogic()

function save_tags(tags) {
    $.ajax({
        type : "POST",
        url : "save_ORs_of_ANDs_hashtags",
        data : {
            'tags' : tags,
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : success,
        error : failure,
    });
}// end save_hashtags()

function success() {
}// end success()

function failure() {
}// end failure()