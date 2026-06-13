#!/usr/bin/env bash
# install.sh — detect GPU, install Mawari node, configure systemd.
set -euo pipefail
REPO="${MAWARI_REPO:-Mawari-Network/mawari-node}"
VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep -m1 '"tag_name"' | cut -d'"' -f4)
VERSION="${VERSION#v}"
ARCH=$(uname -m); case "$ARCH" in x86_64) B=amd64 ;; aarch64) B=arm64 ;; *) echo "bad arch"; exit 1 ;; esac
URL="https://github.com/${REPO}/releases/download/v${VERSION}/mawari-node-${VERSION}-linux-${B}.tar.gz"
echo "==> installing mawari-node v${VERSION}"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
curl -fsSL "$URL" -o "$TMP/m.tgz"
tar -xzf "$TMP/m.tgz" -C "$TMP"
install -m 0755 "$TMP/mawari-node" /usr/local/bin/mawari-node

# Pre-flight: GPU check
echo "==> GPU check"
python3 /root/mawari/src/gpu_check.py || echo "WARN: no GPU detected; node will run in CPU mode"

mkdir -p /root/.mawari
[[ -f /root/.mawari/config.toml ]] || cp config.toml.example /root/.mawari/config.toml
if [[ ! -f /root/.mawari/node.key ]]; then
  echo "==> generating node key"
  /usr/local/bin/mawari-node key gen --out /root/.mawari/node.key
fi

if command -v systemctl >/dev/null && systemctl --no-pager status >/dev/null 2>&1; then
  cp mawari.service /etc/systemd/system/mawari.service
  systemctl daemon-reload
  systemctl enable --now mawari
  echo "==> service installed: mawari (systemd)"
fi
mawari-node --version
