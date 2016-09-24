var gulp            = require('gulp'),
    stylus          = require('gulp-stylus'),
    autoPrefixer    = require('gulp-autoprefixer'),
    plumber         = require('gulp-plumber'),
    browserSync     = require('browser-sync').create();


var paths = {
    css:    'src/css/**/*.styl',
    html:   'src/*.html',
    js:     'src/js/*.js',
    img:    'src/img/*'
}


// Task html
gulp.task('html', function() {
    gulp.src(paths.html)
        .pipe(gulp.dest('app/'));
    browserSync.reload()
});

// Task style
// Stylus, preprocess
gulp.task('style', function() {
    gulp.src(paths.css)
        .pipe(plumber())
        .pipe(stylus({
            compress: false
        }))
        .pipe(autoPrefixer({
            browsers: ['last 3 versions']
        }))
        .pipe(gulp.dest('app/css'))
        .pipe(browserSync.reload({stream:true}));
});

// Task js
gulp.task('js', function() {
    gulp.src(paths.js)
        .pipe(gulp.dest('app/js'));
    browserSync.reload()
});

// Task image
gulp.task('image', function() {
    gulp.src(paths.img)
        .pipe(gulp.dest('app/img'));
});

// Task watch
gulp.task('watch', function() {
    browserSync.init({
        server: './app',
        open: false
    });

    gulp.watch(paths.css, ['style']);
    gulp.watch(paths.html, ['html']);
    gulp.watch(paths.js, ['js']);
    gulp.watch(paths.img, ['image']);
});

// Task default
gulp.task('default', ['html', 'style', 'js', 'image', 'watch']);
