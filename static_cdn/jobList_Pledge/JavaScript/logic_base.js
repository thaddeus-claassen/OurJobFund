$('document').ready(function() {                                        //Wait until document is ready (what defines as ready, I don't know)
    addCol();
    addCol();
    $('#apply_metric').click(function() {
        applyMetric();
    });
    $('#cancel_metric').click(function() {
        close();
    });
});

function mainInputFunction(input) {
    var textID = $(input).attr('id');                               //      Create new variable textID and set it to the ID of the input clicked on
    var nameTemplate = textID.substring(0,10);                      //      Create new variable nameTemplate, which stores a template for each ID of any row
    var rowNumber = 0;                                              //      Create new variable rowNumber and set it to zero. This variable keeps track of the current rowNumber we are looking at (we will iterate through all of them)
    var tempRow = nameTemplate + "1";                               //      Create new variable tempRow and set it to the ID of the first row
    var numEmptyRows = 0;                                           //      Create 
    while ($('#' + tempRow).length > 0) {
        rowNumber++;
        tempRow = nameTemplate + rowNumber.toString();
        if ($('#' + tempRow).val() == '') {
            numEmptyRows++;
        }// end if
    }// end while
    var groupID = textID.substring(0,6);
    if (numEmptyRows <= 2) {
        addInnerSpan(groupID, rowNumber);
        addRow(groupID, rowNumber);
    }// end if
    var shouldAddCol = colShouldBeAdded(groupID);
    if (shouldAddCol) {
        addCol();
    }// end if
}// end mainInputFunction() 

function colShouldBeAdded(currCol) {
    var prevColsContainInput = true;
    var tempCol = findNumCol();
    while(prevColsContainInput && (tempCol > 0)) {
        var tempColID = 'group' + tempCol;
        if (tempColID != currCol) {
            var colHasInput = colContainsInput(tempColID);
            if (colHasInput) {
                tempCol--;
            } else {
                prevColsContainInput = false;
            }// end if-else
        } else {
            tempCol--;
        }// end if-else
    }// end while
    return prevColsContainInput;
}// end colShouldBeAdded()

function colContainsInput(colID) {
    var colHasInput = false;
    var currRow = 1;
    while (!colHasInput && ($('#' + colID + 'text' + currRow).length > 0)) {
        var currInput = $('#' + colID + 'text' + currRow).val();
        if (currInput == '') {
            currRow++;
        } else {
            colHasInput = true;
        }// end if-else
    }// while
    return colHasInput;
}// end colContainsInput()

function findNumCol() {
    var numCol = 1;
    while ($('#' + 'group' + numCol).length > 0) {
        numCol++;
    }// end while
    numCol--;
    return numCol;
}// end findNumCol()

function addCol() {
    var numCols = findNumCol();
    addOuterSpan(numCols);
    addTable(numCols);

    var groupID = "group" + (numCols + 1);
    addRow(groupID, 1);
//    addInnerSpan(groupID, 2);
//    addRow(groupID, 2);
//    addInnerSpan(groupID, 3);
//    addRow(groupID, 3);
}// end addCol()

function addTable(numCols) {
    $('#logic_screen').append('<table id="group' + (numCols + 1) + '" class="logic_group"></table>');
}// end addTable()

function addRow(groupID, rowNumber) {
    var rowID = groupID + 'row' + rowNumber;
    var textID = groupID + 'text' + rowNumber;
    var rowString = '<tr class="logic_text" id="' + rowID + '"><td><input id="' + textID + '" type="text" size="25" onclick="mainInputFunction(this)" /></td></tr>';
    $(rowString).appendTo('#' + groupID);
}// end addRow()

//function applyMetric() {
//    $.ajax {
//        type : 'POST';
//        url: 'apply_hashtags';
//        data: {
//            "hashtags" : getHashtagsString();
//        }
//    }// end ajax
//}// end applyMetric()

















