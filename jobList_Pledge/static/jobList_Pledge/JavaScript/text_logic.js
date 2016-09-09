$('document').ready(function() {
        // Text bar opacity
        $(':text').focusin(function() {
            $(this).attr('value', '').css('opacity', 1);
        });

        $(':text').blur(function() {
            var org = this.getAttribute("value");
            $(this).attr('value', "org" ).css('opacity', 0.5);
        });
        // End text bar opacity
    });
