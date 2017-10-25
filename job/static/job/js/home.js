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
    $('#show_filter').click(function() {
        $(this).css('display', 'none');
        $('#advanced-settings-wrapper').css('display', 'inline');
        $('#hide_filter').css('display', 'inline');
    });
    $('#hide_filter').click(function() {
        $(this).css('display', 'none');
        $('#show_filter').css('display', 'block');
        $('#advanced-settings-wrapper').css('display', 'none');
    });
    $('#show_location').click(function() {
        $(this).css('display', 'none');
        $('.show_location').css('display', 'block');
        $('#hide_location').css('display', 'block');
    });
    $('#hide_location').click(function() {
        $(this).css('display', 'none');
        $('.show_location').css('display', 'none');
        $('#show_location').css('display', 'block');
    });
    $('#basic').click(function() {
        $('#basic_search_jobs').css('display', 'inline');
        $('#custom_search_jobs').css('display', 'none');
    });
    $('#custom').click(function() {
        $('#basic_search_jobs').css('display', 'none');
        $('#custom_search_jobs').css('display', 'inline');
    });
    $('#basic_search_jobs').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
    });
    $('#search_button').click(function() {
        search();
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
    $('tbody').scroll(function() {
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight) {
            if (50 * numSearches <= parseInt($('#num-jobs-found').text())) {
                add_jobs();
            }// end if
        }// end if
    });
});

function search() {
    clearMarkers();
    numSearches = 0;
    if ($('#location').val() == "") {
        get_jobs();
    } else {
        applyLocation();
    }// end if-else
    get_total_jobs();
}// end search()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function get_jobs() {
    var search_type = $("input[name='search']:checked").val();
    $.ajax({
        url : 'get_jobs',
        data : {
            'search_type' : search_type,
            'search' : $('#' + search_type + '_search_jobs').val(),
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
    var search_type = $("input[name='search']:checked").val();
    $.ajax({
        url : 'get_total_jobs',
        data : {
            'search_type' : search_type,
            'search' : $('#' + search_type + '_search_jobs').val(),
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
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < markers.length; i++) {
        bounds.extend(markers[i].getPosition());
    }// end for
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: position.coords.latitude, lng: position.coords.longitude},
        zoom: 12,
    });
    map.fitBounds(bounds);
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
