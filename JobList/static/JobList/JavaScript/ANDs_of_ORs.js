function getURL() {
    return "get_ANDs_of_ORs_tags";
}// end getURL()

function applyMetric() {
    var string = getHashtagsString();
    save_tags(string);
}// end applyMetric()

function addOuterSpan(numCols) {
    if (numCols > 0) {
        $('#group' + numCols).after('<span id="group' + numCols + 'span" class="outside_clause">AND</span>');
    }// end if
}// end addOuterSpan()

function addInnerSpan(groupID, rowNumber) {
    $('#' + groupID).append('<tr id="' + groupID + "row" + (rowNumber - 1) + 'span"><td><span class="inside_clause" style="display: inline;">OR</span></td></tr>');
}// end addInnerSpan()

function innerLogic() {
    return '|';
}// end innerLogic()

function outerLogic() {
    return '&';
}// end outerLogic()

function save_tags(tags) {
    $.ajax({
        type : "POST",
        url : "save_ANDs_of_ORs_hashtags",
        data : {
            'tags' : tags,
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : function(){},
        error : function(){},
    });
}// end save_hashtags()
