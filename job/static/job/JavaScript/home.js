var pi = 3.14159265;
var center;
var numSearches = 0;
var ENTER = 13;

$('document').ready(function() {
    $('.sort').click(function() {
        var by = $(this).attr('id');
        var sort_by_val =  $('#sort').val();
        if (sort_by_val.indexOf(by) !== -1) {
            if (sort_by_val.includes('descending')) {
                sort_by_val = by + ' ascending';
            } else {
                sort_by_val = by + ' descending';
            }// end if-else
        } else {
            if (by === 'name') {
                sort_by_val = by + ' ascending';
            } else {
                sort_by_val = by + ' descending';
            }// end if-else
        }// end if-else
        $('#sort').val(sort_by_val);
        sort_jobs();
    });
    $('.related-to-location').keydown(function(event) {
        if (event.which == ENTER) {
            numSearches = 0;
            if ($('#location').val() == "") {
                get_jobs();
            } else {
                applyLocation();
            }// end if-else
            get_total_jobs();
        }// end if
    });
    $('#search_jobs').keydown(function(event) {
        if (event.which == ENTER) {
            numSearches = 0;
            if ($('#location').val() == "") {
                get_jobs();
            } else {
                applyLocation();
            }// end if-else
            get_total_jobs();
        }// end if
    });
    $('#search_button').click(function(event) {
        numSearches = 0;
        if ($('#location').val() == "") {
            get_jobs();
        } else {
            applyLocation();
        }// end if-else
        get_total_jobs();
    });
     $(window).scroll(function(){
        if ($(window).scrollTop() == $(document).height()-$(window).height()) {
            if (50 * numSearches <= parseInt($('#num-jobs-found').text())) {
                add_jobs();
            }// end if
        }// end if
    });
});

function get_jobs() {
    $.ajax({
        url : 'get_jobs',
        data : {
            'search' : $('#search_jobs').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : $('#radius').val(),
            'sort' : $('#sort').val(),
        },
        success: getJobsSuccess,
    });
}// end get_jobs()

function add_jobs() {
    $.ajax({
        url : 'add_jobs',
        data : {
            'numSearches' : numSearches,
            'search' : $('#search_jobs').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : $('#radius').val(),
            'sort' : $('#sort').val(),
        },
        success: addJobsSuccess,
    });
}// end add_jobs()

function sort_jobs() {
    $.ajax({
        url : 'sort_jobs',
        data : {
            'numSearches' : numSearches,
            'search' : $('#search_jobs').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : $('#radius').val(),
            'sort' : $('#sort').val(),
        },
        success: sortJobsSuccess,
    });
}// end sort_jobs()

function get_total_jobs() {
    $.ajax({
        url : 'get_total_jobs',
        data : {
            'search' : $('#search_jobs').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : $('#radius').val(),
            'sort' : $('#sort').val(),
        },
        success: getTotalJobs,
    });
}// end get_total_jobs()

function getTotalJobs(json) {
    $('#num-jobs-found').text(json['total']);
}// end getTotalJobs()

function getJobsSuccess(json) {
    numSearches = 1;
    $('#main_table_body').empty();
    var numJobs = addJobsToTable(json);
}// end getJobsSuccess()

function addJobsSuccess(json) {
    numSearches = numSearches + 1;
    var numJobs = addJobsToTable(json);
}// end addJobs()

function sortJobsSuccess(json) {
    $('#main_table_body').empty();
    addJobsToTable(json);
    var sort = $('#sort').val();
    var type = sort[0];
    var a_or_d = sort[1];
    
}// end sortJobs()

function addJobsToTable(json) {
    var numJobs = Object.keys(json).length;
    if (numJobs > 0) {
        for (var index = 0; index < json.length; index++) {
            var job = json[index];
            var fields = job["fields"];
            var string = "<tr><td><a href='" + fields["random_string"] + "'>";
            string = string + fields["name"] + "</a></td>";
            string = string + "<td>" + fields['creation_date'] + "</td>";
            string = string + "<td>" + fields['money_pledged'] + "</td>";
            string = string + "<td>" + fields['num_workers'] + "</td></tr>";
            $('#main_table_body').append(string);
        }// end for
    }// end if
    return numJobs;
}// end addJobsToTable

function toggleAdvancedSearch() {
    $('#toggle-advanced-settings').click(function(event) {
        event.preventDefault();
        $('#wrapper').toggleClass('advancedSettingsDisplayed');
    });
}// end toggleAdvancedSearch()

function applyLocation() {
    var address = $('#location').val();
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            center = results[0].geometry.location;
            $('#latitude').val(center.lat());
            $('#longitude').val(center.lng());
            get_jobs();
        }// end if
    });
}// end applyLocation()
