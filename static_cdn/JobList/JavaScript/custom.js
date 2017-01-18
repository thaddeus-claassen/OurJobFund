var opacity = 0.75;
var originalText = 'ex: (#eagles | #birds) || (#washingtonDC & - #swamps)';
$('document').ready(function() {
    getTextFromUser();
    $('#custom-logic').css('opacity', opacity);
    $('#custom-logic').focusout(function() {
       if ($('#custom-logic').val() == "") {
           $('#custom-logic').val(originalText);
           $('#custom-logic').css('opacity', opacity);
       }// end if
    });
    $('#custom-logic').focus(function() {
        if ($('#custom-logic').val() == originalText && $('#custom-logic').css('opacity') == opacity) {
            $('#custom-logic').css('opacity', 10);
            $('#custom-logic').val("");
        }// end if
    });
    $('#apply-metric').click(function(event) {
        event.preventDefault();
        applyMetric();
        document.location.href = 'index';
    });
    $('#cancel-metric').click(function() {
        document.location.href = 'index';
    });
});

function getTextFromUser() {
    $.ajax({                                                                                                              
        type : "GET",                                                          
        url : "get_custom_tags",                                           
        success : function(data) {
            $('#custom-logic').val(data);
        },                                                                                                  
    });
}// end getTextFromUser()

function applyMetric() {
    var logic = $('#custom-logic').val();
    logic = replaceLogic(logic);
    save_custom_tags(logic);
}// end applyMetric()

function replaceLogic(logic) {
    logic = replaceANDs(logic);
    logic = replaceORs(logic);
    logic = replaceNOTs(logic);
    logic = replaceSpaces(logic);
    return logic;
}// end replaceLogic()

function replaceANDs(logic) {
    logic = logic.replace(/&&/g, '&');
    return logic;
}// end replaceANDs()

function replaceORs(logic) {
    logic = logic.replace(/\|\|/g, '|');
    return logic;
}// end replaceANDs()

function replaceNOTs(logic) {
    logic = logic.replace(/-/g, '~');
    logic = logic.replace(/!/g, '~');
    return logic;
}// end replaceANDs()

function replaceSpaces(logic) {
    logic = logic.replace(/\s/g, '');
    return logic;
}// end replaceSpaces()

function save_custom_tags(logic) {
    $.ajax({                                                                                                              
        type : "POST",                                                          
        url : "save_custom_tags",                                           
        data : {                                                                
            'tags' : logic,                 
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(), 
        },
        success : function(){},                                                 
        error : function(){},                                                   
    });
}// end applyHashtags()


