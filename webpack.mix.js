let mix = require('laravel-mix');
let tailwindcss = require('tailwindcss');

mix.js('src/app.js', 'assets/');

mix.sass('src/app.scss', 'assets/')
.options({
  processCssUrls: false,
  postCss: [ tailwindcss('./tailwind.js') ],
});

mix.copy('node_modules/@mdi/font/fonts', 'fonts');
