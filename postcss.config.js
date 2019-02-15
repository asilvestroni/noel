var tailwindcss = require('tailwindcss');
var postcssimport = require('postcss-import');

module.exports = {
    plugins: [
        postcssimport(),
        tailwindcss('./tailwind.js'),
        require('autoprefixer'),
    ]
};
