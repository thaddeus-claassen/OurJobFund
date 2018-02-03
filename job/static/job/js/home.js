var center;
var numSearches = 0;
var ENTER = 13;
var map;
var markers = [];

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    toggleSearch();
    $('input[name=search]').change(function() {
        toggleSearch();
        save_search_type(($(this).attr('id') === 'basic_search'));
    });
    showLocation();
    $('#show-location').change(function() {
        showLocation();
    });
    $('#basic_search').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
    });
    $('#search_button').click(function() {
        search();
    });
    $('#location').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
    });
    $('#radius').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
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
    $(document).on('input', 'input:text', function() {
        if ($(this).attr('class') === 'filter' && !isNaN($(this).val())) {
            save_filter($(this));
        }// end if
    });
});

function search() {
    clearMarkers();
    numSearches = 0;
    applyLocation();
}// end search()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function save_filter(filter) {
    $.ajax({
        type : 'POST',
        url : '/job/save-filter/',
        data : {
            'filter' : $(filter).attr('id'),
            'value' : $(filter).val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
    });
}// end save_filter()

function save_search_type(isBasic) {
    $.ajax({
        type : 'POST',
        url : '/job/save-search-type/',
        data : {
            'isBasic' : isBasic,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
    });
}// end save_search_type()

function save_show_location(isHidden) {
    $.ajax({
        type : 'POST',
        url : '/job/save-show-location/',
        data : {
            'isHidden' : isHidden,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
    });
}// end save_show_location()

function get_jobs() {
    var id = $('input[name="search"]:checked').attr('id');
    var lat = "";
    var lng = "";
    if ($('#show-location').prop('checked')) {
        lat = $('#latitude').val();
        lng = $('#longitude').val();
    }// end if
    $.ajax({
        url : 'job/get-jobs',
        data : {
            'type' : id,
            'search' : $('#' + id +'_search').val(),
            'latitude' : lat,
            'longitude' : lng,
            'radius' : getRadius(),
            'sort' : $('#sort').val(),
        },
        success: getJobsSuccess,
    });
}// end get_jobs()

function add_jobs() {
    var id = $('input[name="search"]:checked').attr('id');
    var lat = "";
    var lng = "";
    if ($('#show-location').prop('checked')) {
        lat = $('#latitude').val();
        lng = $('#longitude').val();
    }// end if
    $.ajax({
        url : 'job/add-jobs',
        data : {
            'numSearches' : numSearches,
            'type' : id,
            'search' : $('#' + id +'_search').val(),
            'latitude' : lat,
            'longitude' : lng,
            'radius' : getRadius(),
            'sort' : $('#sort').val(),
        },
        success: addJobsSuccess,
    });
}// end add_jobs()

function sort_jobs() {
    var id = $('input[name="search"]:checked').attr('id');
    var lat = "";
    var lng = "";
    if ($('#show-location').prop('checked')) {
        lat = $('#latitude').val();
        lng = $('#longitude').val();
    }// end if
    $.ajax({
        url : 'job/sort_jobs',
        data : {
            'numSearches' : numSearches,
            'type' : id,
            'search' : $('#' + id +'_search').val(),
            'latitude' : lat,
            'longitude' : lng,
            'radius' : getRadius(),
            'sort' : $('#sort').val(),
        },
        success: sortJobsSuccess,
    });
}// end sort_jobs()

function get_total_jobs() {
    var id = $('input[name="search"]:checked').attr('id');
    var lat = "";
    var lng = "";
    if ($('#show-location').prop('checked')) {
        lat = $('#latitude').val();
        lng = $('#longitude').val();
    }// end if
    $.ajax({
        url : 'job/get-total-jobs',
        data : {
            'type' : id,
            'search' : $('#' + id +'_search').val(),
            'latitude' : lat,
            'longitude' : lng,
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
            var string = "<tr>"
            string = string + "<td class='name'><a id='" + job["random_string"] + "' href='" + job["random_string"] + "'></a></td>";
            string = string + "<td class='date'>" + job['creation_date'] + "</td>";
            string = string + "<td class='pledged-paid'><sup>$" + turnMoneyToString(job['expected_pay']) + "</sup>&frasl;";
            string = string + "<sub>$" + turnMoneyToString(job['paid']) + "</sub></td>";
            string = string + "<td class='workers-finished'><sup>" + job['expected_workers'] + "</sup>&frasl;<sub>" + job['finished'] + "</sub></td>"
            string = string + "</tr>";
            $('#main_table_body').append(string);
            $('#' + job["random_string"]).text(job["name"]);
            if ($('#location').val() != "") {
                addMarker(new google.maps.LatLng(job['latitude'], job['longitude']), job["random_string"]);    
            }// end if
        }// end for
    }// end if
    if ($('#location').val() != "") {
        addBounds();
    }// end if
    return numJobs;
}// end addJobsToTable()

function applyLocation() {
    var address = $('#location').val();
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            center = results[0].geometry.location;
            $('#latitude').val(center.lat());
            $('#longitude').val(center.lng());
            get_jobs();
            get_total_jobs();
        } else {
            get_jobs();
            get_total_jobs();
        }// end if-else
    });
}// end applyLocation()

function getRadius() {
    var radius = parseFloat($('#radius').val());
    if (isNaN(radius)) {
        radius = 10;
    }// end if
    return radius
}// end getRadius()

function initMap() {
    map = new google.maps.Map(document.getElementById('map'));
    var bounds = new google.maps.LatLngBounds();
    bounds.extend({lat: 25.7617, lng: -80.1918});
    bounds.extend({lat: 32.7157, lng: -117.1611});
    bounds.extend({lat: 21.9, lng: -160.2});
    bounds.extend({lat: 71.3, lng: -156.8});
    map.fitBounds(bounds);
}// end initMap()

function addBounds() {
    map.setZoom(1)
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < markers.length; i++) {
        bounds.extend(markers[i].position);
        map.fitBounds(bounds);
    }// end for
    if (map.zoom > 15) map.setZoom(15)
}// end addBounds()

function addMarker(location, url) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        url: url,
    });
    google.maps.event.addListener(marker, 'click', function() {
        window.location.href = this.url;
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

function turnMoneyToString(number) {
    parts = number.toString().split('.');
    if (parts.length == 1) {
        number = number.toString() + ".00";
    } else {
        if (parts[1].length == 1) {
            number = number.toString() + "0";
        }// end if
    }// end if-else
    return number.toString();
}// end turnMoneyToString()

function toggleSearch() {
    if ($('#basic').prop('checked')) {
        $('#basic_search').css('display', 'inline');
        $('#custom_search').css('display', 'none');
    } else {
        $('#basic_search').css('display', 'none');
        $('#custom_search').css('display', 'inline');
    }// end if-else
}// end toggleSearch()

function showLocation() {
    if ($('#show-location').prop('checked')) {
        $('#location-wrapper').css('display', 'inline');
    } else {
        $('#location-wrapper').css('display', 'none');
    }// end if-else
}// end showLocation()
