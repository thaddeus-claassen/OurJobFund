var pi = 3.14159265;
var basicTagInput = "";
var map;
var center;
$('document').ready(function() {
    addNumJobsToSpan(0);
	disableBasicTagsInput();	
    $('#logout').click(function() {
        logout();
    });
    $('[name=tag-radio]').change(function() {
        disableBasicTagsInput();
    });
    $('#search_bar').keydown(function(event) {
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
    $('#table-border').resizable();
    // If someone types tags into the basic search bar
    $('#basic_tags_input').keydown(function(event) {    // If a key was pressed 
        if (event.which == 13) {                            // If the pressed key is ENTER
            event.preventDefault();                         // Prevent the page from changing (I think due to the form element?)
            filterByTagsAndLocation();
        }// end if
    });
    $('#location-checkbox').change(function() {
        if ($(this).prop('checked')) {
            $('.location-hide').css('display', 'inline');
            $('#empty-space').css('height', '0px');
        } else {
            $('.location-hide').css('display', 'none');
            $('#empty-space').css('height', '100px');
        }// end if-else
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
            filterByTagsAndLocation();
        }// end if-else
    }); 
});

function logout() {
    $.post("/pledge/logout_pledge/");
}// end logout()

function filterByTagsAndLocation() {
    $.ajax ({
        url : "apply_tags_and_location",
        data : {
            'locationTrue' : $('#location-checkbox').prop('checked'),
            'typeOfTags' : getTagsRadio(),
            'basicTags' : $('#basic_tags_input').val(),
            'latitude' : findLat(),
            'longitude' : findLng(),
            'radius' : findRadius(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : searchSuccess,
        error : searchFailure,
    });
}// end filterByTagsAndLocation()

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
            center = results[0].geometry.location;
            map.setCenter(center);
            filterByTagsAndLocation();
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

function findLat() {
    var lat = null;
    if ($('#location-checkbox').prop('checked')) {
        lat = center.lat();
        lat = lat * pi / 180;
    }// end if
    return lat;
}// end findLat()

function findLng() {
    var lng = null;
    if ($('#location-checkbox').prop('checked')) {
        center.lng();
        lng = lng * pi / 180;
    }// end if
    return lng;
}// end findLon()

function searchJobsByRadiusSuccess(json) {
    searchSuccess(json);
}// end searchJobsByRadiusSuccess()

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
