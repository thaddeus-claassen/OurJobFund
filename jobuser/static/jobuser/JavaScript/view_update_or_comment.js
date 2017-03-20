$('document').ready(function() {
    $('#write_a_comment').click(function() {
        $('#write_comment_modal').css('display', 'inline');
    });
    $('.close_modal').click(function() {
        $('#write_comment_modal').css('display', 'none');
    });
    $('#publish_comment').click(function() {
        publish_comment();
    });
});

function publish_comment() {
    $.ajax({
        type : "POST",
        url : 'publish_comment',
        data : {
            'is_update' : isUpdate(),
            'id' : getID(),
            'image' : $('#add_image').val(),
            'is_complaint' : $('input[name="is_complaint"]:checked').val(),
            'comment' : $('#comment_textarea').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : publishCommentSuccess,
    });
}// end publish_comment()

function publishCommentSuccess() {
    $('#write_comment_modal').css('display', 'none');
    $('#write_a_comment').css('display', 'none');
}// end publishCommentSuccess()