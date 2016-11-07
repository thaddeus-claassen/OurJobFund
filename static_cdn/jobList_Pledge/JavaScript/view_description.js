$('document').ready(function() {
    alert("Document is ready");
    $('#view-description').click(function(event) {
        alert("Clicked on view-description");
        event.preventDefault();
        window.open("/jobList_Pledge/view-description");
    }); 
});