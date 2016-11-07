$('document').ready(function() {
    $('#search_jobs').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            search_jobs();
        }// end if
    });
});

function search_jobs() {
    $.ajax({
        type : "POST",
        url : "search_jobs",
        data : {
            'job_name_or_id' : $('#search_bar').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : searchSuccess,
        error : searchFailure,
    });
}

function searchSuccess(json) {
    $('#main_table').empty();
    if (Object.keys(json).length > 0) {
        for (var index = 0; index < json.length; index++) {
            var job = json[index];
            var pk = job["pk"];
            $('#main_table').prepend("<tr class='row' id='job" + pk + "'></tr>");
            var jobID = '#job' + pk.toString(); 
            var fields = job["fields"];
            $(jobID).append("<td class='col-md-6'> Job name: <a href='" + pk + "'> " + fields["name"] + "</a></td>");
            $(jobID).append("<td class='col-md-3'> $ Pledged: $" + fields["money_pledged"] + "</td>");
            $(jobID).append("<td class='col-md-3'> Workers: " + fields["num_people_doing_job"] + "</td>");
        }// end for
    }// end if
}// end searchSuccess()

function searchFailure(xhr,errmsg,err) {
    console.warn(xhr.responseText)
}// end searchFailure()