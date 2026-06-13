#!/usr/bin/env bash
set -euo pipefail
if screen -ls | grep -q '\.mawari-node'; then screen -S mawari-node -X quit; echo "stopped"; else echo "not running"; fi
