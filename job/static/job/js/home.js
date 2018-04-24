var center;
var numSearches = 0;
var ENTER = 13;
var map;
var markers = [];
var sort = "created-descending";

$('document').ready(function() {
    changeTHeadTFootWidthToAccountForScrollBar();
    $(window).resize(function() {
        changeTHeadTFootWidthToAccountForScrollBar();
    });
    $('#search').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
    });
    $('#location').keydown(function(event) {
        if (event.which == ENTER) {
            search();
        }// end if
    });
    $('.table-header').click(function() {
        var cls = $(this).parent().attr('class');
        setSortAndNumSearches(cls.split("-")[0]);
        get_jobs();
    });
    $('tbody').scroll(function() {
        if ($(this).scrollTop() + $(this).height() === $(this)[0].scrollHeight) {
            if (50 * numSearches <= parseInt($('#num-jobs-found').text())) {
                numSearches = numSearches + 1;
                get_jobs();
            }// end if
        }// end if
    });
    $(document).on('input', 'input:text', function() {
        if ($(this).attr('class') === 'filter' && !isNaN($(this).val())) {
            save_filter($(this));
        }// end if
    });
});

function setSortAndNumSearches(col) {
    if (sort.split("-")[0] === col) {
        if (sort.split("-")[1] === "descending") {
            sort = sort.split("-")[0] + "-ascending";
        } else {
            sort = sort.split("-")[0] + "-descending";
        }// end if-else
    } else {
        numSearches = 1;
        if (col === "date") {
            sort = col + "-descending";
        } else {
            sort = col + "-ascending";
        }// end if-else
    }// end if-else
}// end setSortAndNumSearches()

function search() {
    $('#latitude').val("");
    $('#longitude').val("");
    clearMarkers();
    numSearches = 1;
    applyLocation();
}// end search()

function changeTHeadTFootWidthToAccountForScrollBar() {
    var oldTableWidth = $('table').width();
    var newTableWidth = oldTableWidth - 17;
    var percentageTableWidth = 100 * (newTableWidth / oldTableWidth);
    $('thead').width(percentageTableWidth.toString() + '%');
    $('tfoot').width(percentageTableWidth.toString() + '%');
}// end changeTHeadTFootWidthToAccountForScrollBar()

function get_jobs() {
    $.ajax({
        url : 'job/get-jobs',
        data : {
            'numSearches' : numSearches,
            'search' : $('#search').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : 10,
            'sort' : sort,
        },
        success: function(json) {
            if (numSearches == 1) {
                $('tbody').empty();
                clearMarkers();
            }// end if
            addJobsToTable(json);
        },
        error: function () {
            $('#search-error-message').text("Invalid Search");
        },
    });
}// end get_jobs()

function get_total_jobs() {
    $.ajax({
        url : 'job/get-total-jobs',
        data : {
            'search' : $('#search').val(),
            'latitude' : $('#latitude').val(),
            'longitude' : $('#longitude').val(),
            'radius' : 10,
            'sort' : sort,
        },
        success: function(json) {
            $('#num-jobs-found').text(json['total']);
        },
    });
}// end get_total_jobs()

function addJobsToTable(json) {
    $('#search-error-message').text('');
    for (var index = 0; index < json.length; index++) {
        var job = json[index];
        var string = "<tr>";
        string = string + "<td class='title'><a id='" + job["random_string"] + "' href='job/" + job["random_string"] + "'></a></td>";
        string = string + "<td class='date'>" + job['date'] + "</td>";
        string = string + "<td class='pledging'>$" + turnMoneyToString(job['pledging']) + "</sub></td>";
        string = string + "<td class='working'>" + job['working'] + "</td>"
        string = string + "</tr>";
        $('tbody').append(string);
        $('#' + job["random_string"]).text(job["title"]);
        if ($('#location').val() != "") {
            addMarker(new google.maps.LatLng(job['latitude'], job['longitude']), 'job/' + job["random_string"]);    
        }// end if
    }// end for
    if ($('#location').val() !== "") {
        addBounds();
    }// end if
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

function initMap() {
    map = new google.maps.Map(document.getElementById('map'));
    var bounds = new google.maps.LatLngBounds();
    bounds.extend({lat: 25.7617, lng: -80.1918});
    bounds.extend({lat: 32.7157, lng: -117.1611});
    bounds.extend({lat: 21.9, lng: -160.2});
    bounds.extend({lat: 71.3, lng: -156.8});
    map.fitBounds(bounds);
    if ($('#search').val() != '' || $('#location').val() != ''){
        search();
    }// end if
}// end initMap()

function addBounds() {
    map.setZoom(1);
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < markers.length; i++) {
        bounds.extend(markers[i].position);
        map.fitBounds(bounds);
    }// end for
    if (map.zoom > 15) map.setZoom(15);
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