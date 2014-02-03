var assert = require('assert');
assert(process.argv.length == 5, 'node client.js <port or path> <packet size> <packet count>');

var net = require('net');
var crypto = require('crypto');

if (isNaN(parseInt(process.argv[2])) == false)
    var options = {port: parseInt(process.argv[2])};
else
    var options = {path: process.argv[2]};
console.log('options: ' + JSON.stringify(options));

var packetSize = parseInt(process.argv[3]);
assert(!isNaN(packetSize), 'bad packet size');
console.log('packet size: ' + packetSize);

var packetCount = parseInt(process.argv[4]);
assert(!isNaN(packetCount), 'bad packet count');
console.log('packet count: ' + packetCount);

var client = net.connect(options, function() {
    console.log('client connected');
});

var printedFirst = false;
var packet = crypto.randomBytes(packetSize).toString('base64').substring(0,packetSize);
var currPacketCount = 0;
var startTime;
var endTime;
var delta;
client.on('data', function(data) {
    if (printedFirst == false) {
        console.log('client received: ' + data);
        printedFirst = true;
    }
    else {
        currPacketCount += 1;
        if (data.length != packetSize)
            console.log('weird packet size: ' + data.length);
        //console.log('client received a packet: ' + currPacketCount);
    }

    if (currPacketCount < packetCount) {
        if (currPacketCount == 0) {
            startTime = process.hrtime();
        }
        client.write(packet);
    } else {
        client.end();
        endTime = process.hrtime(startTime);
        delta = (endTime[0] * 1e9 + endTime[1]) / 1e6;
        console.log('millis: ' + delta);
    }
});
