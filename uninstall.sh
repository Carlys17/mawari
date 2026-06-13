#!/usr/bin/env bash
set -euo pipefail
if command -v systemctl >/dev/null && systemctl list-unit-files | grep -q mawari.service; then
  systemctl disable --now mawari || true
  rm -f /etc/systemd/system/mawari.service
  systemctl daemon-reload
fi
screen -S mawari-node -X quit 2>/dev/null || true
rm -rf /root/.mawari
rm -f /usr/local/bin/mawari-node
echo "mawari-node removed"
