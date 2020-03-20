let mix = require('laravel-mix');
let tailwindcss = require('tailwindcss');

require('laravel-mix-purgecss');

mix.js('src/app.js', 'assets/');

mix.sass('src/app.scss', 'assets/').options({
  processCssUrls: false,
  postCss: [tailwindcss('./tailwind.js')],
});

mix.purgeCss({
  content: ['index.html', 'src/app.js', 'src/app.scss'],
  css: ['assets/app.css'],
});

mix.copy('node_modules/@mdi/font/fonts', 'fonts');
