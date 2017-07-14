$('document').ready(function() {
    alert('document is ready');
    $('.change').click(function() {
        $('button was clicked');
        var row = $(this).parent();
        alert(row);
        var info = $(row).children('.class', 'info');
        alert(info);
    });
});
