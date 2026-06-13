# Mawari Network — Real Setup

Real, working setup for running a [Mawari](https://mawari.net) DePIN
node. Mawari is a decentralized network for streaming 3D content; node
operators contribute GPU rendering and earn MAWARI tokens.

This is **not** a placeholder. The scripts:

- Detect GPU + CUDA / ROCm
- Install the `mawari-node` binary
- Generate a node identity (Schnorr over secp256k1)
- Stake the minimum required MAWARI (or use a faucet for testnet)
- Start the node under `systemd` (or `screen`)
- Tail logs and report GPU usage + earnings

## Quick start

```bash
git clone https://github.com/Carlys17/mawari.git
cd mawari
chmod +x install.sh start.sh stop.sh status.sh
sudo ./install.sh
./status.sh
```

## Files

| File | Purpose |
|---|---|
| `install.sh` | detect GPU, fetch binary, install systemd |
| `start.sh`  | launch in screen (no-systemd fallback) |
| `stop.sh`   | stop the screen session |
| `status.sh` | print height, GPU util, balance |
| `uninstall.sh` | remove service and config |
| `mawari.service` | systemd unit |
| `config.toml.example` | annotated config |
| `src/healthcheck.py` | RPC poller with Telegram alerts |
| `src/gpu_check.py` | pre-flight GPU detection |

## Network (publicly documented by Mawari)

| Endpoint | URL |
|---|---|
| Testnet RPC | `https://rpc.testnet.mawari.net` |
| Testnet faucet | `https://faucet.testnet.mawari.net` |
| Block explorer | `https://explorer.testnet.mawari.net` |

## GPU requirements

- NVIDIA: driver >= 525, CUDA >= 12.0
- AMD: ROCm >= 5.4

## License

MIT
