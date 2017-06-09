import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import posts from './posts';
import comments from './comments';

/* Combine all reducers into one. */
const rootReducer = combineReducers({
    posts:posts,
    comments: comments,
    routing: routerReducer
})

export default rootReducer;
