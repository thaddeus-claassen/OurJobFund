function addOuterSpan(numCols) {
    if (numCols > 0) {
        $('#group' + numCols).after('<span id="group' + numCols + 'span" class="outside_clause">AND</span>');
    }// end if
}// end addOuterSpan()

function addInnerSpan(groupID, rowNumber) {
    $('#' + groupID).append('<tr id="' + groupID + "row" + (rowNumber - 1) + 'span"><td><span class="inside_clause" style="display: inline;">OR</span></td></tr>');
}// end addInnerSpan()

function getHashtagsString() {
    var string = "";
    
    return string;
}// end getHashtagsString()