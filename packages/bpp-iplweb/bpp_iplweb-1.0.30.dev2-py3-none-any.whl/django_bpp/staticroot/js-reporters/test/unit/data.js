var TestEnd = require('../../dist/js-reporters.js').TestEnd
var TestStart = require('../../dist/js-reporters.js').TestStart
var SuiteStart = require('../../dist/js-reporters.js').SuiteStart
var SuiteEnd = require('../../dist/js-reporters.js').SuiteEnd

module.exports = {
  passingTest: new TestEnd('pass', undefined, [], 'passed', 0, []),
  failingTest: new TestEnd('fail', undefined, [], 'failed', 0, [
    new Error('first error'), new Error('second error')
  ]),
  skippedTest: new TestEnd('skip', undefined, [], 'skipped', 0, []),
  todoTest: new TestEnd('todo', undefined, [], 'todo', 0, []),
  startSuite: new SuiteStart('start', 'start', [], []),
  startTest: new TestStart('start', 'start', 'start start'),
  endTest: new TestEnd('end', 'end', 'end end', 'failed', 0,
    [new Error('error')], []),
  endSuite: new SuiteEnd('end', 'end', [], [])
}
