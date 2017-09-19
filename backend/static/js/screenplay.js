var html = "";
$(document).ready(function() {

    $('.screenplay').each(function(index){
	var post = $(this)
	fountain.parse(post.text(), function (output) {
	    html = '<div class="title-page">'+output.html.title_page+'</div>' + output.html.script;
	    post.html(html);
	});
    })

});
