#!/usr/bin/env bash
set -euo pipefail
NAME=mawari-node
DATA=${MAWARI_DATA:-/root/.mawari}
LOG=${MAWARI_LOG:-/var/log/mawari.log}
mkdir -p "$(dirname "$LOG")" "$DATA"
if screen -ls | grep -q "\.${NAME}"; then echo "$NAME running"; exit 0; fi
screen -dmS "$NAME" /bin/bash -c "mawari-node run --config $DATA/config.toml 2>&1 | tee -a $LOG"
sleep 2
screen -ls | grep "$NAME" || { echo "failed"; exit 1; }
