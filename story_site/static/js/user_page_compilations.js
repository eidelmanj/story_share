var numTimesRequested = 0;


// TODO - Check if this still works???
window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
	
	$.ajax({
	    method: "GET",
	    url: "/story_site/get_compilations",
	    data: { pageNum : numTimesRequested}
	})
	    .done(function( msg ) {
		$("#prev_compilations_div").append(msg);
	    });
    }
    
};



// Give a personal rank to a compilation
function rank_compilation(compilation, rank) {
    $.ajax({
	method: "GET", //TODO - Security issue? Maybe should be POST
	url: "/story_site/rank_compilation",
	data: { compilation_id : compilation,
		rank : rank }
    });
    return false;
}



// Give a personal rank to a story
function rank_story(story, rank) {
    $.ajax({
	method: "GET", //TODO - Security issue? Maybe should be POST
	url: "/story_site/rank_story",
	data: { story_id : story,
		rank : rank }
    });
    return false;

}
