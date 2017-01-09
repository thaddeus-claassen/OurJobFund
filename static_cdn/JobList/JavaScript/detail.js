$('document').ready(function() {
    $('#view-description').click(function(event) {
        event.preventDefault();
        var jobID = $(this).attr('class');    
        window.open("/jobList_Pledge/" + jobID + "/description");
    }); 
});