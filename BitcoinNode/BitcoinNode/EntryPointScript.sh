#!/bin/bash

# "exec" replaces the shell by bitcoind, so that bitcoind runs as PID 1 and receives the SIGTERM of "docker stop" directly.
# Without it the shell would not forward the signal and bitcoind would be killed without a clean shutdown.
exec bitcoind -datadir=/Workspace/Data -debuglogfile=/Workspace/Logs/BitcoinLogfile.log
