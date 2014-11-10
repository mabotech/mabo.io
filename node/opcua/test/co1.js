
var co = require('co');
var fs = require('fs');

function read(file) {
  return function(fn){
    fs.readFile(file, 'utf8', fn);
  }
}

co(function *(){
  var a = yield read('test1.js');
  var b = yield read('test2.js');
  var c = yield read('test3.js');
  console.log(a);
  console.log(b);
  console.log(c);
})()