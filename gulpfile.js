const cp = require('child_process')
const gulp = require('gulp')
const ghPages = require('gulp-gh-pages')
const imagemin = require('gulp-imagemin')

const image = () => {
  return gulp.src('images/**/*')
      .pipe(imagemin())
      .pipe(gulp.dest('_site/images'))
}

const circleci = () => {
  return gulp.src('.circleci/*')
    .pipe(gulp.dest('_site/.circleci'))
}

const pushGHSource = () => cp.spawn('git', ['push', 'origin', 'source'], { stdio: 'inherit' })

const pushGHPages = () => {
  return gulp.src('_site/**/*')
             .pipe(ghPages({ branch: 'master' }))
}

const build = () => cp.spawn('bundle', ['exec', 'jekyll', 'build'], { stdio: 'inherit' })

const deploy = gulp.series(build, image, circleci, pushGHSource, pushGHPages)

module.exports = {
  circleci,
  image,
  pushGHSource,
  pushGHPages,
  build,
  deploy
}
