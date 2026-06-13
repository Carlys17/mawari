"""Long-running RPC poller for the Mawari node. Telegram alert on stall."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, urllib.request

def rpc(addr, method, params=None):
    body = json.dumps({"jsonrpc":"1.0","id":"hc","method":method,"params":params or []}).encode()
    req = urllib.request.Request(f"http://{addr}", data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def send_tg(bot, chat, text):
    url = f"https://api.telegram.org/bot{bot}/sendMessage"
    body = json.dumps({"chat_id":chat,"text":text,"parse_mode":"Markdown"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}), timeout=10).read()
    except Exception as e:
        print(f"tg: {e}", file=sys.stderr)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rpc", default=os.getenv("MAWARI_RPC","127.0.0.1:7333"))
    p.add_argument("--interval", type=int, default=60)
    p.add_argument("--tg-bot", default=os.getenv("TG_BOT"))
    p.add_argument("--tg-chat", default=os.getenv("TG_CHAT"))
    args = p.parse_args()
    last_h = -1
    fails = 0
    while True:
        try:
            h = rpc(args.rpc, "getblockcount").get("result", 0)
            p_ = rpc(args.rpc, "getconnectioncount").get("result", 0)
            print(f"[{time.strftime('%H:%M:%S')}] height={h} peers={p_}")
            if h == last_h and p_ == 0:
                msg = f"⚠️ Mawari stalled: h={h} peers=0"
                print(msg)
                if args.tg_bot: send_tg(args.tg_bot, args.tg_chat, msg)
            last_h = h
            fails = 0
        except Exception as e:
            fails += 1
            print(f"err: {e}")
            if fails >= 3 and args.tg_bot:
                send_tg(args.tg_bot, args.tg_chat, f"❌ Mawari RPC down 3x: {e}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
