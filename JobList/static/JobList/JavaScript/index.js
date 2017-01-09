var pi = 3.14159265;
var basicTagInput = "";
var map;
var markers = [];
$('document').ready(function() {
	disableBasicTagsInput();	
    $('[name=tag-radio]').change(function() {
        disableBasicTagsInput();
    });
    $('#search_jobs').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            search_jobs();
        }// end if
    });
    $('text:input').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
        }// end if
    });  
    // If someone types tags into the basic search bar
    $('#basic_tags_input').keydown(function(event) {    // If a key was pressed 
        if (event.which == 13) {                            // If the pressed key is ENTER
            event.preventDefault();                         // Prevent the page from changing (I think due to the form element?)
            applytags();                                // Call applyBasictags() function to do all the tag logic
        }// end if
    });
    $('#view_metrics_pledge').click(function() {
        window.open("/jobList_Pledge/view_all_metrics_pledge");
    });
    $('#location-checkbox').change(function() {
        if ($(this).prop('checked')) {
            $('.location-hide').css('display', 'inline');
            $('#empty-space').css('height', '0px');
			hideRevealLocation();
        } else {
            $('.location-hide').css('display', 'none');
            $('#empty-space').css('height', '100px');
        }// end if-else
    });
	$('[name=distance-time]').change(function() {
		hideRevealLocation();
	});
    map = createMap();
    $('#location-text').keydown(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            applyLocation($(this).val());   
        }// end if
    });
    $('.filter-by-button').click(function() {
        if($(this).hasClass('active')) {
            $(this).removeClass('active');
            $('#main_table').empty();
            
        } else {
            $(this).addClass('active');
            filterByTags();
        }// end if-else
    }); 
});

function searchByTagsAndOrLocation() {
    if ($('#advanced-tags-filter').hasClass()) {
        if ($('#location-checkbox').prop('checked')) {
            
        } else {
            
        }// end if-else
    } else {
        if ($('#location-checkbox').prop('checked')) {
            
        } else {
            
        }// end if-else
    }// end if-else
}// end searchByTagsAndOrLocation()

function filterByTagsAndLocation(latitude, longitude, radius) {
    $.ajax ({
        url : "apply_" + getTagsRadio() + "_and_location",
        data : {
            'tags' : $('#basic_tags_input').val(),
            'latitude' : latitude,
            'longitude' : longitude,
            'radius' : radius,
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : searchSuccess,
        error : searchFailure,
    });
}// end filterByTagsAndLocation()

function filterByTags() {
    $.ajax({
        url : "apply_" + getTagsRadio(),
        data : {
            'tags' : $('#basic_tags_input').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : searchSuccess,
        error : searchFailure,
    });
}// end filterByTags()

function getTagsRadio() {
    var id;
    if ($('#tag_basic_logic').prop('checked')) {
        id = "tag_basic_logic";
    } else if ($('#tag_ANDs_of_ORs_logic').prop('checked')) {
        id = "tag_ANDs_of_ORs_logic";
    } else if ($('#tag_ORs_of_ANDs_logic').prop('checked')) {
        id = "tag_ORs_of_ANDs_logic";
    } else {
        id = "tag_custom_logic";  
    }// end if
    return id;
}// end getTagsRadio()

function disableBasicTagsInput() {
	if ($('#tag_basic_logic').prop('checked')) {
        $('#basic_tags_input').val(basicTagInput);
        $('#basic_tags_input').prop('disabled', false);
    } else if ($('#tag_ANDs_of_ORs_logic').prop('checked')) {
        basicTagInput = $('#basic_tags_input').val();
        $('#basic_tags_input').val("");
        $('#basic_tags_input').prop('disabled', true);
    } else if ($('#tag_ORs_of_ANDs_logic').prop('checked')) {
        basicTagInput = $('#basic_tags_input').val();
        $('#basic_tags_input').val("");
        $('#basic_tags_input').prop('disabled', true);
    } else {
        basicTagInput = $('#basic_tags_input').val();
        $('#basic_tags_input').val("");
        $('#basic_tags_input').prop('disabled', true);   
    }// end if
}// end disableBasicTagsInput()

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
}// end search_jobs()

function createMap() {
    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(0,0),
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    // listen for the window resize event & trigger Google Maps to update too
    $(window).resize(function() {
        // (the 'map' here is the result of the created 'var map = ...' above)
        google.maps.event.trigger(map, "resize");
    });
    return map;
}// end createMap()

function applyLocation(address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var center = results[0].geometry.location;
            map.setCenter(center);
            var radius = findRadius();
            var lat = findLat(center);
            search_jobs_by_radius(lat, lon, radius);
        }// end if
    });
}// end applyLocation()

function findRadius() {
    var unit = $("input[type='radio'][name='radius-unit']:checked").val();
    var radius;
    if (unit == "mi") {
        radius = Number($('#location-radius').val());
    } else {
        radius = 0.621371 * Number($('#location-radius').val());
    }// end if-else
    radius = (radius / 69) * (pi / 180);
    return radius;
}// end findRadius()

function findLat(center) {
    var lat = center.lat();
    lat = lat * pi / 180;
    return lat;
}// end findLat()

function findLon(center) {
    var lon = center.lng();
    lon = lon * pi / 180;
    return lon;
}// end findLon()

function search_jobs_by_radius(latitude, longitude, radius) {
    $.ajax({
        type : "POST",
        url : "search_jobs_by_radius",
        data : {
            'latitude' : latitude,
            'longitude' : longitude,
            'radius' : radius,
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : searchJobsByRadiusSuccess,
        error : searchFailure,
    });
}// end search_jobs_by_radius()

function searchJobsByRadiusSuccess(json) {
    clearMarkers();
    var numJobs = Object.keys(json).length; 
    if (numJobs > 0) {
        for (var index = 0; index < json.length; index++) {
            var job = json[index];
            addMarker(job);
        }// end for
    }// end if
    searchSuccess(json);
}// end searchJobsByRadiusSuccess()

// Adds a marker to the map and push to the array.
function addMarker(job) {
    var fields = job["fields"];
    var name = fields['name'];
    var latitude = fields['latitude'] * (180 / pi); 
    var longitude = fields['longitude'] * (180 / pi);    
    var latLng = {lat: latitude, lng: longitude};
    var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        title: name,
    });
    markers.push(marker);
    setMapOnAll()
}// end addMarker()

// Sets the map on all markers in the array.
function setMapOnAll() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }// end for
}// end setMapOnAll()

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}// end clearMarkers()

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}// end showMarkers()

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}// end deleteMarkers()

function searchSuccess(json) {    
    $('#main_table').empty();
    var numJobs = Object.keys(json).length; 
    if (numJobs > 0) {
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
    addNumJobsToSpan(numJobs);
}// end searchSuccess()

function addNumJobsToSpan(numJobs) {
    $('#found-x-jobs').text(numJobs);
}// end addNumJobsToSpan()

function searchFailure(xhr,errmsg,err) {
    console.warn(xhr.responseText);
}// end searchFailure()

// This function handles the AJAX call to refresh the table without refreshing the page 
//  when someone presses enter into the basic tags form
function applytags() {
    $.ajax({                                                                    // Creates new AJAX function with JQuery?                                               
        type : "POST",                                                          // tag form is done with POST. Chose that only because I could get it to work
        url : "apply_tag_basic_logic",                                           // Defines which URL to send the form to. (I think this is where the tags are sent to Django, but I am not 100% sure)
        data : {                                                                // Defines what the data is, which Django will use
            'tags' : $('#basic_tags_input').val(),                      // Gives the Django 'tags' variable value of all of the tags inputted by the user
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(), // I don't know what this does really. Something to do with CSRF, which I mention in the HTML document "index.html", but I don't know why I need to mention it here
        },
        success : basicSuccess,                                                 // Calls the method basicSuccess if the AJAX works properly
        error : basicFailure,                                                   // Calls the method basicFailure if AJAX failed somewhere along the line
    });
}// end applytags()


////////////////////// Still working on code form here -------------------> ...
function applyBasictags() {
    var tags = $('#basic_tags_input').val();
    tags = tags.replace(/\,/g,"");
    return tags;
}// applyBasictags()

// This function is called when AJAX works properly
function basicSuccess(json) {                                                       // Takes in JSON as a parameter. I do not know how that gets there when the call to basicSuccess is in data and does not specify JSON. Maybe the call comes from Django directly. I don't really know.
    $('#main_table').empty();                                                       // Remove everything inside of the job table, which was already there
    var numJobs = Object.keys(json).length; 
    if (numJobs > 0) {                                             // Somehow this means "If there is something in the json" I think
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
    $('#found-x-jobs').text(numJobs);
}// end basicSuccess()

// This function is called if there is an error with the AJAX for some reason or another. I do not know which errors call this function and which ones do not
function basicFailure(xhr,errmsg,err) { // I have no idea what these three parameters are
    alert("Basic tag AJAX failed");                 // Alerts the user that AJAX failed
}// end basicFailure()

// ... <---------------------------------------------------------- To here