$(document).ready(function(){

    //Toggle reply
    $('.show-reply').click(function () {
	$('.comment-reply').hide()
	$(this).parent().parent().children('.comment-reply').toggle();
    });
    //cancel
    $('.cancel').click(function () {
	$('.comment-reply').hide()
    });
    


    // Voting
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
    function commentUpvote(commentId) {
	$.ajax({
	    type: "POST",
	    url: "/comment-upvote/",
	    data: {"comment-id": commentId},
	    success: function(){
		var upvoteLink = $('#comment-upvote-'+commentId);
		var score = upvoteLink.parent().find(".score");
                var notUpdated = Number(score.html());
                score.html(notUpdated + 1);
		upvoteLink.addClass('comment-upvoted');		    
		upvoteLink.off("click");
		// upvoteLink.click(function(){ return false;});
		upvoteLink.click(function(){
		    var commentId = parseInt(this.id.split("-")[2]);
		    return commentUnupvote(commentId);
		})
	    },
	    headers: {
		'X-CSRFToken': csrftoken
	    }
	});
	return false;
    }

    

    // Unupvote
    function commentUnupvote(commentId) {
	$.ajax({
	    type: "POST",
	    url: "/comment-unupvote/",
	    data: {"comment-id": commentId},
	    success: function(){
		var upvoteLink = $('#comment-upvote-'+commentId);
		upvoteLink.removeClass('comment-upvoted');
		var score = upvoteLink.parent().find(".score");
                var notUpdated = Number(score.html());
                score.html(notUpdated - 1);
		upvoteLink.off("click");
		// upvoteLink.click(function(){ return false;});
		upvoteLink.click(function(){
		    var commentId = parseInt(this.id.split("-")[2]);
		    return commentUpvote(commentId);
		})
	    },
	    headers: {
		'X-CSRFToken': csrftoken
	    }
	});
	return false;
    }

    
    //Connect functions
    $("a.comment-upvote").click(function(){
	var commentId = parseInt(this.id.split("-")[2]);
	return commentUpvote(commentId);
    })

    // Upvoted
    $("a.comment-upvoted").unbind('click').click(function(){
	var commentId = parseInt(this.id.split("-")[2]);
	console.log("UnUpvote!")
	return commentUnupvote(commentId);
    })
    

    

}); // End document ready
