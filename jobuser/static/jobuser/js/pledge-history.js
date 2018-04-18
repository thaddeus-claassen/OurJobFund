function addRowsToTable(json) {
    $('tbody').empty();
    for (var index = 0; index < json.length; index++) {
        var p = json[index];
        var to, confirmed;
        var type = p['type'];
        if (type === 'Stripe Payment' || type === 'Misc. Payment') {
            to = "<a href='user/'" + p['username'] + ">" + p['to'] + "</a>";
        } else {
            to = 'N/A';
        }// end if-else
        if (type === 'Misc. Payment') {
            confirmed = p['confirmed'];
        } else {
            confirmed = 'N/A';
        }// end if-else
        if (p['amount'] === -1) {
            amount = 'N/A';
        } else {
            amount = changeNumberToCurrency(p['amount']);
        }// end if-else
        var string = "<tr>";
        string = string + "<td class='username'><a href='user/ " + p['username'] + "'>" + p['username'] + "</a></td>";
        string = string + "<td class='date'>" + p['date'] + "</td>";
        string = string + "<td class='type'>" + type + "</td>";
        string = string + "<td class='amount'>" + amount + "</td>";
        string = string + "<td class='to'>" + to + "</td>";
        string = string + "<td class='confirmed'>" + confirmed + "</td>";
        string = string + "</tr>";
        $('tbody').append(string);
    }// end for
}// end addRowsToPledgesTable()