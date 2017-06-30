var html = "";
$(document).ready(function() {
    if ($('.screenplay')[0]) {
	var post = $('.screenplay')[0];
	fountain.parse(post.innerHTML, function (output) {
	    html = '<div class="title-page">'+output.html.title_page+'</div>' + output.html.script;
	    $('.screenplay').eq(0).html(html);
	});
    }
});
