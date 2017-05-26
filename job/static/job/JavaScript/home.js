var pi = 3.14159265;
var center;
var numSearches = 0;
var ENTER = 13;

$('document').ready(function() {
    $('.sort').click(function() {
        var by = $(this).attr('id');
        var sort_by_val =  $('#sort-by').val();
        if (sort_by_val.includes(by)) {
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
        $('#sort-by').val(sort_by_val);
        $('#sort-form').submit();
    });
    $('#search_bar').keydown(function(event) {
        if (event.which == ENTER) {
            $('#sort-form').submit();
        }// end if
    });
     $(window).scroll(function(){
        if ($(window).scrollTop() == $(document).height()-$(window).height()) {
            if (50 * numSearches < parseInt($('#total').val())) {
                see_more_jobs();
            }// end if
        }// end if
    });
});

function see_more_jobs() {         
    $.ajax({
        url : 'see_more_jobs',
        data : {
            'numSearches' : numSearches,
            'search' : $('#search').val(),
            'sort-by' : $('#sort-by').val(),
        },
        success: seeMoreJobsSuccess,
    });
}// end see_more_jobs()

function seeMoreJobsSuccess(json) {
    numSearches = numSearches + 1;
    var numJobs = Object.keys(json).length; 
    if (numJobs > 0) {
        for (var index = 0; index < json.length; index++) {
            var user = json[index];
            var fields = job["fields"];
            var string = "<tr><td> Job name: <a href='" + fields["random_string"] + "'> ";
            var string = string + fields['name'] + "</a></td>";
            var string = string + "<td>" + fields['creation_date'] + "</td>";
            var string = string + "<td>" + fields['money_pledged'] + "</td>";
            var string = string + "<td>" + fields['num_workers'] + "</td></tr>";
            $('#user-table').append(string);
        }// end for
    }// end if
    $('#num-jobs-found').text($('#num-jobs-found').text() + numJobs);
}// end seeMoreJobsSuccess()

function toggleAdvancedSearch() {
    $('#toggle-advanced-settings').click(function(event) {
        event.preventDefault();
        $('#wrapper').toggleClass('advancedSettingsDisplayed');
    });
}// end toggleAdvancedSearch()

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
