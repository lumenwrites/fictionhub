const webpack = require('webpack');
var path = require('path');

function getPlugins() {
    const plugins = [];
    if (process.env.NODE_ENV === "production") {
        plugins.push(new webpack.DefinePlugin({
	    'process.env': {
		NODE_ENV: JSON.stringify('production')
	    }
	}));
        plugins.push(new webpack.optimize.UglifyJsPlugin({
            minimize: true,
            output: {
                comments: false
            },
            compressor: {
                warnings: false
            }
        })); 
    }
    plugins.push(new webpack.ProvidePlugin({
	$: 'jquery',
	jQuery: 'jquery'
    }));

    return plugins;
}

module.exports = {
    entry: [
	'/home/ray/projects/fictionhub/backend/static/js/index.js'
    ],
    output: {
	path: __dirname + '/dist/',
	filename: 'fictionhub.js'
    },
    module: {
	loaders: [
	    {
		exclude: /node_modules/,
		loader: 'babel-loader',
		query: {
		    presets: ['es2015', 'stage-2']
		}
	    },
	]
    },
    plugins: getPlugins(),
    resolve: {
	extensions: ['','.js']
    },
};
