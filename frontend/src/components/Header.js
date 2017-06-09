import React, { Component } from 'react';

class Header extends Component {
    render() {
	return (
	    <header>
		<div className="container">
		    <div className="row">      
			<div className="col-xs-9 search">
			    <a className="logo">
				nexy
			    </a>
			    <div className="tagline">thoughtful discussion for creative and curious</div>
			</div>
			<div className="col-xs-3 main-menu">
			    <div className="right">
				<a className="btn btn-default">
				    Submit
				</a>
			    </div>
			</div>
		    </div>

		    <div className="row subnav">      
			<div className="col-xs-12 filters">
			    <div className="dropdown">
				<a className="btn btn-default">
				    Hot
				</a>
				<ul className="dropdown-menu" role="menu"  id="sorting">
				    <li><a href="hot">Hot</a></li>	    
				    <li><a href="top">Top</a></li>
				    <li><a href="new">New</a></li>
				</ul>	
			    </div>
			    <div className="dropdown">
				<a className="btn btn-default">
				    Category: All
				</a>
				<ul className="dropdown-menu" role="menu" id="category">
				    <li><a href="all">All</a></li>
				</ul>
			    </div>


			    <form action="" method="get" id="search-form">
				<input type="text" className="form-control" id="searchbar"
				       placeholder=""
				       data-provide="typeahead"
				       autocomplete="off"
				       name="query" value=""/>
				<input type='submit' className="hidden"/>
				<i className="fa fa-search" aria-hidden="true"></i>    
			    </form>
			</div>
		    </div>
		</div>
	    </header>
	)
    }
}

export default Header;
