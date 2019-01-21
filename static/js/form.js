var canSubmit = true;

$('document').ready(function() {
    $('#create-job-form').submit(function(event) {
        if (canSubmit) {
            canSubmit = false;
            formContent();
        } else {
            event.preventDefault();
        }// end if-else
    });
});

function formContent() {
    alert("Form content still in form.js...shoot")
}

