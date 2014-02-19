Unix Domains Sockets vs Localhost TCP Sockets
==========

## Introduction
This project is a NodeJS client and server that benchmarks the efficiency benefits of Unix Domain Sockets over TCP Localhost sockets. More information about this project can be found at: <blog url here>

## Running the benchmark
This benchmark application uses the Python taskrun library for running the various benchmarks. More information about taskrun can be found at [https://github.com/nicmcd/taskrun]

Before running the benchmarks, the server must be started:
'''shell
node server.js <tcp port> <domain socket path>
'''

For simplicity sake, the taskrun file is hardcoded to TCP port 5555 and domain socket path /tmp/uds, so you should start your server with:
'''shell
node server.js 5555 /tmp/uds
'''

A single client benchmark can be run with:
'''shell
node client.js <port or path> <packet size> <packet count>
'''

To match the client with the aforementioned server startup, run:
'''shell
node client.js 5555 1000 100000
'''
and
'''shell
node client.js /tmp/uds 1000 100000
'''

Running both of these commands should show that for 1k packets repeated 100,000 times, Unix domain sockets beat localhost TCP sockets by about 3x.

The full benchmark analysis is run with:
'''shell
python run.py
'''
This will take a significant amount of time to run. Mine took about a half hour. Go have fun and come back later.

## Interpreting the results
The taskrun script generates a CSV file in the 'run' directory. Each benchmark point is run 10 times so it is best to average these. I used Microsoft Excel to import the CSV file and generate a graph. My benchmark was run on an Intel E5-2620v2 processor running Ubuntu 13.10.
