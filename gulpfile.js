const cp = require('child_process')
const gulp = require('gulp')
const ghPages = require('gulp-gh-pages')
const imagemin = require('gulp-imagemin')

const image = () => {
  return gulp.src('images/**/*')
      .pipe(imagemin())
      .pipe(gulp.dest('_site/images'))
}

const pushGHSource = () => cp.spawn('git', ['push', 'origin', 'source'], { stdio: 'inherit' })

const pushGHPages = () => {
  return gulp.src('_site/**/*')
             .pipe(ghPages({ branch: 'master' }))
}

const build = () => cp.spawn('bundle', ['exec', 'jekyll', 'build'], { stdio: 'inherit' })

const ghActionsBuild = gulp.series(build, image)

const deploy = gulp.series(build, image, pushGHSource, pushGHPages)

module.exports = {
  image,
  pushGHSource,
  pushGHPages,
  build,
  ghActionsBuild,
  deploy
}
