#!/usr/bin/env bash
set -euo pipefail
DATA=${MAWARI_DATA:-/root/.mawari}
RPC=${MAWARI_RPC:-127.0.0.1:7333}
echo "height : $(mawari-node rpc --rpc=$RPC getblockcount 2>/dev/null || echo n/a)"
echo "peers  : $(mawari-node rpc --rpc=$RPC getconnectioncount 2>/dev/null || echo n/a)"
echo "balance: $(mawari-node rpc --rpc=$RPC getbalance 2>/dev/null || echo n/a)"
echo "node   : $(cat $DATA/node.key.pub 2>/dev/null || echo n/a)"
