import React from 'react';
import { render } from 'react-dom';

/* Import css */
import css from './styles/style.css';

/* Import comonents */
import Main from './components/Main';
import PostList from './components/PostList';
import PostDetail from './components/PostDetail';

/* React Router */
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { Provider } from 'react-redux';

import store, { history } from './store';

const router = (
    <Provider store={store}>
	<Router history={history}>
	    <Route path="/" component={Main}>
		<IndexRoute component={PostList}></IndexRoute>
		<Route path="/post/:postId" component={PostDetail}></Route>
	    </Route>
	</Router>
    </Provider>
)
render (router, document.getElementById('root')); 
