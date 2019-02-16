let mix = require('laravel-mix');
let tailwindcss = require('tailwindcss');

mix.js('src/app.js', 'docs/assets/');

mix.sass('src/app.scss', 'docs/assets/')
.options({
  processCssUrls: false,
  postCss: [ tailwindcss('./tailwind.js') ],
});

mix.copy('node_modules/@mdi/font/fonts', 'docs/fonts');
