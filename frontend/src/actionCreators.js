// upvote
export function upvote(postId) {
    return {
	type: 'UPVOTE_POST',
	postId: postId
    }
}

// add comment
export function addComment(postId, author, comment) {
    return {
	type: 'ADD_COMMENT',
	postId: postId,
	author: author,
	comment: comment
    }    
}

// delete comment
export function deleteComment(commentId) {
    return {
	type: 'DELETE_COMMENT',
	commentId: commentId
    }        
}
