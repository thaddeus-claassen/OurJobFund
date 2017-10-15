function addJobsToTable(json) {
    var numJobs = Object.keys(json).length;
    if (numJobs > 0) {
        for (var index = 0; index < json.length; index++) {
            var job = json[index];
            var string = "<tr><td class='name'><a href='" + job["random_string"] + "'>";
            string = string + job["name"] + "</a></td>";
            string = string + "<td class='date'>" + job['creation_date'] + "</td>";
            string = string + "<td class='pledged'>$" + job['pledged'] + "</td>";
            string = string + "<td class='paid'>$" + job['paid'] + "</td>";
            string = string + "<td class='workers'>" + job['workers'] + "</td>";
            string = string + "<td class='expected_workers'>" + job['expected_workers'] + "</td>";
            string = string + "<td class='finished'>" + job['finished'] + "</td></tr>";
            $('#main_table_body').append(string);
            if ($('#location').val() != "") {
                addMarker(new google.maps.LatLng(job['latitude'], job['longitude']));    
            }// end if
        }// end for
    }// end if
    return numJobs;
}// end addJobsToTable()