var assert = require('assert');
assert(process.argv.length == 4, 'node server.js <tcp port> <domain socket path>');

var net = require('net');

var tcpPort = parseInt(process.argv[2]);
assert(!isNaN(tcpPort), 'bad TCP port');
console.log('TCP port: ' + tcpPort);

var udsPath = process.argv[3];
console.log('UDS path: ' + udsPath);

function createServer(name, portPath) {
    var server = net.createServer(function(socket) {
        console.log(name + ' server connected');
        socket.on('end', function() {
            console.log(name + ' server disconnected');
        });
        socket.write('start sending now!');
        socket.pipe(socket);
    });
    server.listen(portPath, function() {
        console.log(name + ' server listening on ' + portPath);
    });
}

var tcpServer = createServer('TCP', tcpPort);
var udsServer = createServer('UDS', udsPath);
