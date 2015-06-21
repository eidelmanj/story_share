var global_selected_tags = [];


$(function (ready) {
    $("#country_select").change(function () {
	get_cities($("#country_select").val());
    });

    $("#tag_input").keypress( function (e) {

	if (e.which==13) {
	    global_selected_tags.push($("#tag_input").val());
	    $("#tag_input").val("");
	    display_tags();
	}
    });


    $(function() {
	$( "#tag_input" ).autocomplete({
	    source: get_available_tags()
	});
    });
    

    
})


function get_available_tags() {
    // TODO
    return [ "test" ];
}


function display_tags() {
    $("#tag_display").html("");
    var tagHtmlStr="";

    for (tag in global_selected_tags) {
	tagHtmlStr+="<a href='#' onclick=remove_tag('"+global_selected_tags[tag]+"')>x</a>. "+global_selected_tags[tag]+", ";
    }
    
    $("#tag_display").html(tagHtmlStr);
}


function remove_tag(tag) {
    global_selected_tags.splice(global_selected_tags.indexOf(tag), 1);
    display_tags();
}


function get_cities(country_name) {
    if (country_name=="None") {
	$("#city_td").html("");
	return;
    }
	
    
    var request = $.ajax({
	url: "/story_site/get_cities",
	method: "GET",
	data: { country : country_name },
	dataType: "html"
    });
    
    request.done(function( msg ) {
	$("#city_td").html(msg);
    });

    request.fail(function( jqXHR, textStatus ) {
	alert( "Request failed: " + textStatus );
    });
}




function submit_form() {
    var tableHtml = ""

    var jsonTags = JSON.stringify(global_selected_tags);
    tableHtml+="<input type='hidden' name='tags' value='"+jsonTags+"'>";

    $("#extra_stuff_div").html(tableHtml);
    $("#compile_form").submit()
    
}
