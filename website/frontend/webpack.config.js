const path = require('path');
const webpack = require('webpack');

module.exports = {
    mode: 'development',
    entry: {
        'main': './src/js/main.js',
    },
    output: {
        path: path.resolve(__dirname, "..", 'static'),
        filename: '[name].js'
    },
    plugins: [
        // Have this example work in Edge which doesn't ship `TextEncoder` or
        // `TextDecoder` at this time.
        new webpack.ProvidePlugin({
          TextDecoder: ['text-encoding', 'TextDecoder'],
          TextEncoder: ['text-encoding', 'TextEncoder']
        })
    ]
};