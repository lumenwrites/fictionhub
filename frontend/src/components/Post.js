import React, { Component } from 'react';

class Post extends Component {
    render() {
	return (
	    <article>
		<div className="post-header">    
		    <h2>{this.props.title}</h2>
		</div>
		
		<div className="post-body">  
		    <p>
			{this.props.body}
		    </p>
		</div>

		<div className="clearfix"></div>
		<div className="post-footer">
		    <span className="label label-default"><a>Tag</a></span>
		    <span className="right">@rayalez</span>
		    <span className="right">shownexy.io</span>    
		</div>

		
	    </article>
	)
    }
}

export default Post;
