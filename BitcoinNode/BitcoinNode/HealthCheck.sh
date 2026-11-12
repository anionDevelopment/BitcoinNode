#!/bin/bash
set -o errexit

# The node is considered healthy if bitcoind answers RPC-requests.
# bitcoin-cli reads the RPC-credentials (cookie-file or rpcuser/rpcpassword in bitcoin.conf) from the data-folder.
bitcoin-cli -datadir=/Workspace/Data getnetworkinfo > /dev/null
echo "Healthy: bitcoind answers RPC-requests."
