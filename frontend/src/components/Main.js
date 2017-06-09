import React from 'react';
import { Link } from 'react-router';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as actionCreators from '../actionCreators';

import Header from './Header';
import Footer from './Footer';

const Main = React.createClass({
    render() {
	/* cloneElement allows to pass props to children, otherwise it wouldn't work */
	return (
	    <div>
		<Header />
		<div className="container">		
		    {React.cloneElement(this.props.children, this.props)}
		    <Footer />
		</div>
	    </div>
	)
    }
})


function mapStateToProps(state) {
    return {
	posts: state.posts,
	comments: state.comments
    }
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
