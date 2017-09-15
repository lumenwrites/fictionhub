import React, { Component } from 'react';

import Post from './Post';

class PostList extends Component {

    renderPosts() {
	const posts = this.props.posts;

	if (!posts) { return <div></div>; };

	return posts.map((post) => {
	    return (
		<Post key={post.slug}
		      title={post.title}
		      body={"Post body"}
		      tags={["One","Two"]}
		      link={`post/${post.slug}`}/>
	    )
	});
    }

    render() {
	return (
	    <div className="row">
		<div className="col-md-12 col-sm-12">
		    { this.renderPosts() }
		</div>
	    </div>
	)
    }
}


export default PostList;
