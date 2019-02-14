var debug = process.env.NODE_ENV !== "production";

module.exports = {
    mode: debug ? "development" : "production",
    context: __dirname,
    entry: "./assets/styles/app.scss",
    output: {
        path: __dirname + "/main/static/main"
    },
    optimization: {
        minimize: !!debug
    },
    module: {
		rules: [
			{
				test: /\.(s*)css$/,
				use: [
					{
						loader: 'file-loader',
						options: {
							name: "styles.css"
						}
					},
					{
						loader: 'extract-loader'
					},
					{
						loader: 'css-loader?-url'
					},
					{
						loader: 'sass-loader'
					},
                    {
                        loader: 'postcss-loader'
                    }
				]
			}
		]
    }
};