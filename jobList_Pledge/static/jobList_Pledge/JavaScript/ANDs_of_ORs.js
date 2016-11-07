function addOuterSpan(numCols) {
    $('#group' + numCols).after('<span id="group' + numCols + 'span" class="outside_clause">AND</span>');
}// end addOuterSpan()

function addInnerSpan(groupID, rowNumber) {
    $('#' + groupID).append('<tr id="' + groupID + "row" + (rowNumber - 1) + 'span"><td><span class="inside_clause">OR</span></td></tr>');
}// end addInnerSpan()

function getHashtagsString() {
    var string = "";
    
    return string;
}// end getHashtagsString()