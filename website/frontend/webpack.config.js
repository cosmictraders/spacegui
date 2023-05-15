const {resolve} = require("path");
const webpack = require("webpack");

module.exports = {
    mode: 'development',
    entry: {
        'main': './src/main.js',
    },
    output: {
        path: resolve(__dirname, "..", 'static'),
        filename: '[name].js'
    }
}
