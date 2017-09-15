import React, { Component } from 'react';

class Header extends Component {
    render() {
	return (
	    <footer>
		<hr/>
		<div className="right">
		    Made by <a href="http://rayalez.com">Ray Alez</a>
		    <a href="https://github.com/raymestalez/nexy">
			<i className="fa fa-github"></i>
		    </a>
		</div>
	    </footer>
	)
    }
}

export default Header;
