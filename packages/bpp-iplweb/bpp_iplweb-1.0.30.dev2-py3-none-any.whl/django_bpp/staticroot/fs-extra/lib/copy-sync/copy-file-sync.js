var fs = require('graceful-fs')

var BUF_LENGTH = 64 * 1024
var _buff = new Buffer(BUF_LENGTH)

function copyFileSync (srcFile, destFile, options) {
  var clobber = options.clobber
  var preserveTimestamps = options.preserveTimestamps

  if (fs.existsSync(destFile)) {
    if (clobber) {
      fs.unlinkSync(destFile)
    } else {
      var err = new Error('EEXIST: ' + destFile + ' already exists.')
      err.code = 'EEXIST'
      err.errno = -17
      err.path = destFile
      throw err
    }
  }

  var fdr = fs.openSync(srcFile, 'r')
  var stat = fs.fstatSync(fdr)
  var fdw = fs.openSync(destFile, 'w', stat.mode)
  var bytesRead = 1
  var pos = 0

  while (bytesRead > 0) {
    bytesRead = fs.readSync(fdr, _buff, 0, BUF_LENGTH, pos)
    fs.writeSync(fdw, _buff, 0, bytesRead)
    pos += bytesRead
  }

  if (preserveTimestamps) {
    fs.futimesSync(fdw, stat.atime, stat.mtime)
  }

  fs.closeSync(fdr)
  fs.closeSync(fdw)
}

module.exports = copyFileSync
