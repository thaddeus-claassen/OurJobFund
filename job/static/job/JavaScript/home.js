var center;
var numSearches = 0;
var ENTER = 13;
var map;
var markers = [];
var MILES_TO_KILOMETERS = 1.60934;

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
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
    $('.search').keydown(function(event) {
        if (event.which == ENTER) {
            clearMarkers();
            numSearches = 0;
            if ($('#location').val() == "") {
                get_jobs();
            } else {
                applyLocation();
            }// end if-else
            get_total_jobs();
        }// end if
    });
    $('tbody').scroll(function() {
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight) {
            if (50 * numSearches <= parseInt($('#num-jobs-found').text())) {
                add_jobs();
            }// end if
        }// end if
    });
});

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

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
            'radius' : getRadius(),
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
            'radius' : getRadius(),
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
            'radius' : getRadius(),
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
    clearMarkers();
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
            var string = "<tr><td class='name'><a href='" + fields["random_string"] + "'>";
            string = string + fields["name"] + "</a></td>";
            string = string + "<td class='date'>" + fields['creation_date'] + "</td>";
            string = string + "<td class='pledged'>$" + fields['pledged'] + "</td>";
            string = string + "<td class='paid'>$" + fields['paid'] + "</td>";
            string = string + "<td class='workers'>" + fields['workers'] + "</td>";
            string = string + "<td class='finished'>" + fields['finished'] + "</td></tr>";
            $('#main_table_body').append(string);
            if ($('#location').val() != "") {
                addMarker(new google.maps.LatLng(fields['latitude'],fields['longitude']));    
            }// end if
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

function getRadius() {
    var radius = parseFloat($('#radius').val());
    if (radius == NaN) {
        radius = 100;
    } else {
        if ($('#km').is(':checked')) {
            radius = MILES_TO_KILOMETERS * radius;
        }// end if
    }// end if-else
    return radius
}// end getRadius()

function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(centerMap)
    } else {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 0, lng: 0},
            zoom: 1,
        });
    }
}// end initMap()

function centerMap(position) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: position.coords.latitude, lng: position.coords.longitude},
        zoom: 12,
    });
}// centerMap()

function addMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
    markers.push(marker);
}// end addMarker()

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }// end for
}// end setMapOnAll()

function clearMarkers() {
    setMapOnAll(null);
}// end clearMarkers()

function deleteMarkers() {
    clearMarkers();
    markers = [];
}// end deleteMarkers()
