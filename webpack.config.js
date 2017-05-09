var path = require("path");

module.exports = {
    entry: {
        input: "./django_rest/static/jsx/main.jsx",
        table: "./django_rest/static/jsx/table_handler.jsx"
    },
    output: {
        path: path.join(__dirname, "./django_rest/static/js"),
		filename: "[name].bundle.js",
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react']
                }
            }
        ]
    }
}

