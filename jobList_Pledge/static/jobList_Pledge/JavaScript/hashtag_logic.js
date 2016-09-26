// Handles the logic for all of the hashtag search forms (basic, ANDs of ORs, ORs of ANDs, custom)
$('document').ready(function() {
    $('#basic_hashtags_input').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            applyBasicHashtags();
        }// end if
    });
    $('#hashtag_ANDs_of_ORs_logic').click(function(event) {
        window.open("/jobList_Pledge/ANDs_of_ORs/");  
    });
});

function applyBasicHashtags() {
    $.ajax({
        type : "POST",
        url : "apply_basic_hashtags",
        data : {
            'hashtags' : $('#basic_hashtags_input').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : basicSuccess,
        error : basicFailure,
    });
}

function basicSuccess(json) {
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
}// end basicSuccess()

function basicFailure(xhr,errmsg,err) {
    alert("It failed");
}// end basicFailure()