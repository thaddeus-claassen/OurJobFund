$('document').ready(function() {                                        //Wait until document is ready (what defines as ready, I don't know)
    addCol();
    addCol();
    $('#apply-metric').click(function(event) {
        event.preventDefault();
        applyMetric();
        document.location.href = 'index';
    });
    $('#cancel-metric').click(function() {
        document.location.href = 'index';
    });
});

function mainInputFunction(input) {
    var textID = $(input).attr('id');                               //      Create new variable textID and set it to the ID of the input clicked on
    var rowArray = findRows(textID);
    var rowNumber = rowArray[0];
    var numEmptyRows = rowArray[1];
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

function findRows(textID) {
    var rowNumber = 0;                                              //      Create new variable rowNumber and set it to zero. This variable keeps track of the current rowNumber we are looking at (we will iterate through all of them)
    var nameTemplate = textID.substring(0,10);                      //      Create new variable nameTemplate, which stores a template for each ID of any row
    var tempRow = nameTemplate + "1";                               //      Create new variable tempRow and set it to the ID of the first row
    var numEmptyRows = 0;                                           //      Create 
    while ($('#' + tempRow).length > 0) {
        rowNumber++;
        tempRow = nameTemplate + rowNumber.toString();
        if ($('#' + tempRow).val() == '') {
            numEmptyRows++;
        }// end if
    }// end while
    return [rowNumber, numEmptyRows];
}// end findRows()

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
    addInnerSpan(groupID, 2);
    addRow(groupID, 2);
    addInnerSpan(groupID, 3);
    addRow(groupID, 3);
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

function getHashtagsString() {
    var string = '';
    var numCols = findNumCol();
    for (var col = 1; col <= numCols; col++) {
        var colString = '';
        var textID = 'group' + col.toString();
        var row = 1;
        while ($('#' + textID + 'row' + row.toString()).length > 0) {
            var tag = $('#' + textID + 'text' + row.toString()).val(); 
            if (tag != '') {
                if (colString == '') {
                    colString = '(';
                } else {
                    colString += innerLogic();
                }// end if-else
                colString += tag;
            }// end if
            row++;
        }// end while
        if (colString != '') {
            colString += ')';
            if (string != '') {
                string += outerLogic();
            }// end if
            string += colString;
        }// end if
    }// end for
    return string;
}// end getHashtagsString()














