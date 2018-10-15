'use strict';

/**
 * Load npm modules
 */
const gulp = require('gulp');
const babel = require('gulp-babel');
const concat = require('gulp-concat');
const imagemin = require('gulp-imagemin');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const uglify = require('gulp-uglify');

/**
 * Paths Styles.
 */
const stylesWatch = ['./src/static/src/sass/**/*'];
const stylesSrc = [
  './node_modules/jquery-bar-rating/dist/themes/fontawesome-stars-o.css',
  './node_modules/cookieconsent/src/styles/**/*.css',
  './src/static/src/sass/main.scss'
];
const stylesDest = './src/static/dist/css/';

/**
 * Paths scripts.
 */
const scriptsWatch = ['./src/static/src/js/**/*.js'];
const scriptsSrc = ['./src/static/src/js/**/*.js'];
const scriptsDest = './src/static/dist/js/';

/**
 * Paths scripts de terceros.
 */
const scriptsThirdSrc = [
  './node_modules/jquery/dist/jquery.js',
  './node_modules/tether/dist/js/tether.js',
  './node_modules/bootstrap/dist/js/bootstrap.js',
  './node_modules/toastr/toastr.js',
  './node_modules/jquery-bar-rating/jquery.barrating.js',
  './node_modules/js-cookie/src/js.cookie.js',
  './node_modules/cookieconsent/src/cookieconsent.js',
  './node_modules/select2/dist/js/select2.full.min.js'
];

/**
 * Paths Images.
 */
const imagesSrc = ['./src/static/src/img/**/*'];
const imageDest = './src/static/dist/img';
const imagesWatch = imagesSrc;

/******************************************************************************
 * Tareas Copy files.
 *****************************************************************************/
gulp.task('copy', () => {
  /**
   * Fuentes.
   *
   * Copia archivos de node_modules u otros sitios a src/static/dist/xx
   *
   * Material icons se ha de descargar manualmente.
   * @ver: src/static/src/sass/_material-icons.scss.
   */
  // font-awesome.
  gulp.src(['./node_modules/components-font-awesome/fonts/**/*'])
    .pipe(gulp.dest('./src/static/dist/fonts/font-awesome'));

  // Roboto fonts.
  gulp.src(['./node_modules/roboto-fontface/fonts/Roboto/*'])
    .pipe(gulp.dest('./src/static/dist/fonts/roboto'));

  /**
   * Imágenes.
   *
   * Copiar imágenes que no requieran compresión.
   * Si requieren de compresión, usar gulp.task('images', () => {})
   */
});

/******************************************************************************
 * Tareas Styles.
 *****************************************************************************/

/**
 * Sass desarrollo.
 *
 * No minifica el archivo main.css.
 */
gulp.task('styles:dev', () => {
  gulp.src(stylesSrc)
    .pipe(concat('main.css'))
    .pipe(sourcemaps.init())
      .pipe(sass())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(stylesDest));
});

/**
 * Sass producción.
 *
 * Minifica el archivo main.css.
 */
gulp.task('styles:prod', () => {
  gulp.src(stylesSrc)
    .pipe(concat('main.min.css'))
    .pipe(sass({outputStyle: 'compressed'}))
    .pipe(gulp.dest(stylesDest));
});

/*****************************************************************************
 * Tareas Javascript locales.
 *****************************************************************************/

/**
 * Javascript locales, desarrollo.
 *
 * Archivos locales no minificados.
 */
gulp.task('scripts:local:dev', () => {
  gulp.src(scriptsSrc)
    .pipe(concat('main.js'))
    .pipe(sourcemaps.init())
      .pipe(babel({
        presets: ['es2015']
      }))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(scriptsDest));
});

/**
 * Javascript locales, producción.
 *
 * Archivos locales minificados.
 */
gulp.task('scripts:local:prod', () => {
  gulp.src(scriptsSrc)
    .pipe(concat('main.min.js'))
    .pipe(babel({
      presets: ['es2015']
    }))
    .pipe(uglify())
    .pipe(gulp.dest(scriptsDest));
});

/******************************************************************************
 * Tareas Javascript terceros.
 *****************************************************************************/
/**
 * Javascript terceros, desarrollo.
 *
 * Archivos de terceros no minificados.
 */
gulp.task('scripts:third:dev', () => {
  gulp.src(scriptsThirdSrc)
    .pipe(concat('vendor.js'))
    .pipe(sourcemaps.init())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(scriptsDest));
});

/**
 * Javascript terceros, producción.
 *
 * Archivos de terceros minificados.
 */
gulp.task('scripts:third:prod', () => {
  gulp.src(scriptsThirdSrc)
    .pipe(concat('vendor.min.js'))
    .pipe(uglify({
      output: {
        max_line_len: 100000
      }
    }))
    .pipe(gulp.dest(scriptsDest));
});

/******************************************************************************
 * Tareas images.
 *****************************************************************************/
gulp.task('images', () => {
  gulp.src(imagesSrc)
    .pipe(imagemin())
    .pipe(gulp.dest(imageDest));
});

/******************************************************************************
 * Watches.
 *
 * Solo son para archivos locales y desarrollo.
 *****************************************************************************/

// Watch styles.
gulp.task('watch:styles', () => {
  gulp.watch(stylesWatch, ['styles:dev']);
});

// Watch scripts.
gulp.task('watch:scripts', () => {
  gulp.watch(scriptsWatch, ['scripts:local:dev']);
});

// Watch images.
gulp.task('watch:images', () => {
  gulp.watch(imagesWatch, ['images']);
});

// Watches
gulp.task('watches', () => {
  gulp.watch(stylesWatch, ['styles:dev']);
  gulp.watch(scriptsWatch, ['scripts:local:dev']);
  gulp.watch(imagesWatch, ['images']);
});

/******************************************************************************
 * Commands.
 *****************************************************************************/
/**
 * Genera archivos para desarrollo y producción.
 * copy no tiene watch, por lo que se ha de generar al menos una vez.
 */
gulp.task('default', [
  'copy',
  'images',
  'styles:prod',
  'styles:dev',
  'scripts:third:prod',
  'scripts:third:dev',
  'scripts:local:prod',
  'scripts:local:dev'
]);
