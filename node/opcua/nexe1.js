var nexe = require('nexe');

nexe.compile({
    input: 'main.js',
    output: 'bin',
    nodeVersion: '0.11.14',
    nodeTempDir: __dirname,
    flags: true
}, function(err) {

});