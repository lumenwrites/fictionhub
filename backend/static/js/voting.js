$(document).ready(function(){
    // getting csrf token.
    function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
	    var cookies = document.cookie.split(';');
	    for (var i = 0; i < cookies.length; i++) {
		var cookie = jQuery.trim(cookies[i]);
		// Does this cookie string begin with the name we want?
   		if (cookie.substring(0, name.length + 1) == (name + '=')) {
		    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		    break;
		}
	    }
	}
	return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Upvote
    function upvote(postId) {
	$.ajax({
	    type: "POST",
	    url: "/upvote/",
	    data: {"post-id": postId},
	    success: function(){
		// After successful upvote
		// Highlight upvoted
		var upvoteLink = $('#post-upvote-'+postId);
		upvoteLink.addClass('upvoted');
		// Increment Score
		var scoreSpan = upvoteLink.parent().find(".score");
		var score = parseInt(scoreSpan.html());
		scoreSpan.html(score + 1);
		// Unbind upvote function, replace it with unupvote
		upvoteLink.off("click");
		upvoteLink.unbind('click').click(function(){
		    var postId = parseInt(this.id.split("-")[2]);
		    console.log("Upvote!")
		    return unupvote(postId);
		})
	    },
	    headers: {
		'X-CSRFToken': csrftoken
	    }
	});
	return false;
    }

    

    // Unupvote
    function unupvote(postId) {
	$.ajax({
	    type: "POST",
	    url: "/unupvote/",
	    data: {"post-id": postId},
	    success: function(){
		// After successful unupvote
		// Remove highlight
		var upvoteLink = $('#post-upvote-'+postId);
		upvoteLink.removeClass('upvoted');
		upvoteLink.off("click");
		// Decrement score
		var scoreSpan = upvoteLink.parent().find(".score");
		var score = parseInt(scoreSpan.html());
		scoreSpan.html(score - 1);
		// Unbind unupvote function, replace it with upvote
		upvoteLink.unbind('click').click(function(){
		    var postId = parseInt(this.id.split("-")[2]);
		    console.log("UnUpvote!")		    
		    return upvote(postId);
		})
	    },
	    headers: {
		'X-CSRFToken': csrftoken
	    }
	});
	return false;
    }

    //Connect functions
    $("a.upvote").unbind('click').click(function(){
	var postId = parseInt(this.id.split("-")[2]);
	console.log("Upvote!")
	return upvote(postId);
    })

    // Upvoted
    $("a.upvoted").unbind('click').click(function(){
	var postId = parseInt(this.id.split("-")[2]);
	console.log("UnUpvote!")
	return unupvote(postId);
    })

})
