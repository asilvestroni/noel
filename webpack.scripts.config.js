const webpack = require('webpack');
const debug = process.env.NODE_ENV !== "production";

module.exports = {
    mode: debug ? "development" : "production",
    context: __dirname,
    devtool: debug ? "inline-sourcemap" : false,
    entry: "./assets/scripts/app.ts",
    plugins: [
        new webpack.ProvidePlugin({fetch: 'imports?this=>global!exports?global.fetch'})
    ],
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loader: 'babel-loader',
            },
        ],
    },
    resolve: {
        extensions: ['.ts', '.js']
    },
    output: {
        path: __dirname + "/main/static/main",
        filename: "scripts.min.js"
    },
    optimization: {
        minimize: !!debug
    }
};