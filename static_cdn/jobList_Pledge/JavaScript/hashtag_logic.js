// Handles the logic for all of the hashtag search forms (basic, ANDs of ORs, ORs of ANDs, custom)
$('document').ready(function() {
    // If someone types hashtags into the basic search bar
    $('#basic_hashtags_input').keydown(function(event) {    // If a key was pressed 
        if (event.which == 13) {                            // If the pressed key is ENTER
            event.preventDefault();                         // Prevent the page from changing (I think due to the form element?)
            applyHashtags();                           // Call applyBasicHashtags() function to do all the hashtag logic
        }// end if
    });
    $('#hashtag_ANDs_of_ORs_logic').click(function(event) { // If someone wanted the ANDs_of_ORs hashtag template rather than the basic one
        window.open("/jobList_Pledge/ANDs_of_ORs");         // Open /jobList_Pledge/ANDs_of_ORs/ in a NEW tab
    });
});

// This function handles the AJAX call to refresh the table without refreshing the page 
//  when someone presses enter into the basic hashtags form
function applyHashtags() {
    $.ajax({                                                                    // Creates new AJAX function with JQuery?                                               
        type : "POST",                                                          // Hashtag form is done with POST. Chose that only because I could get it to work
        url : "apply_basic_hashtags",                                           // Defines which URL to send the form to. (I think this is how the hashtags are sent to Django, but I am not 100% sure)
        data : {                                                                // Defines what the data is, which Django will use
            'hashtags' : $('#basic_hashtags_input').val(),                      // Gives the Django 'hashtags' variable value of all of the hashtags inputted by the user
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(), // I don't know what this does really. Something to do with CSRF, which I mention in the HTML document "index.html", but I don't know why I need to mention it here
        },
        success : basicSuccess,                                                 // Calls the method basicSuccess if the AJAX works properly
        error : basicFailure,                                                   // Calls the method basicFailure if AJAX failed somewhere along the line
    });
}// end applyHashtags()


////////////////////// Still working on code form here -------------------> ...
function applyBasicHashtags() {
    var hashtags = $('#basic_hashtags_input').val();
    hashtags = hashtags.replace(/\,/g,"");
}// applyBasicHashtags()

// This function is called when AJAX works properly
function basicSuccess(json) {                                                       // Takes in JSON as a parameter. I do not know how that gets there when the call to basicSuccess is in data and does not specify JSON. Maybe the call comes from Django directly. I don't really know.
    $('#main_table').empty();                                                       // Remove everything inside of the job table, which was already there
    if (Object.keys(json).length > 0) {                                             // Somehow this means "If there is something in the json" I think
        for (var index = 0; index < json.length; index++) {                         // Get the index for each json element
            var job = json[index];                                                  // Then get that element, which is a job
            var pk = job["pk"];                                                     // Save the primary key of the job
            $('#main_table').prepend("<tr class='row' id='job" + pk + "'></tr>");   // Add a row to the job table
            var fields = job["fields"];                                             // Get the values of the three fields
            // The next three line saves the next three data points of the table into a single string
            var string = "<td class='col-md-6'> Job name: <a href='" + pk + "'> " + fields["name"] + "</a></td>";
            string += "<td class='col-md-3'> $ Pledged: $" + fields["money_pledged"] + "</td>";
            string += "<td class='col-md-3'> Workers: " + fields["num_people_doing_job"] + "</td>";
            $('#job' + pk.toString()).append(string);                              // Add the three data points to the job row
        }// end for
    }// end if
}// end basicSuccess()

// This function is called if there is an error with the AJAX for some reason or another. I do not know which errors call this function and which ones do not
function basicFailure(xhr,errmsg,err) { // I have no idea what these three parameters are
    alert("Basic Hashtag AJAX failed");                 // Alerts the user that AJAX failed
}// end basicFailure()

// ... <---------------------------------------------------------- To here