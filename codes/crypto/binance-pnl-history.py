def run(api_key: str = "", api_secret: str = "", symbol: str = "BTCUSDT"):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    symbol: Futures pair (default: BTCUSDT)
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    from datetime import datetime
    if not api_key or not api_secret:
        print("❌ api_key, api_secret 필요. recall('binance api')로 조회하세요.");return
    BASE="https://fapi.binance.com"
    params={"symbol":symbol.upper(),"limit":"50","timestamp":str(int(time.time()*1000))}
    qs=urllib.parse.urlencode(params)
    sig=hmac.new(api_secret.encode(),qs.encode(),hashlib.sha256).hexdigest()
    req=urllib.request.Request(f"{BASE}/fapi/v1/userTrades?{qs}&signature={sig}")
    req.add_header("X-MBX-APIKEY",api_key)
    try:
        with urllib.request.urlopen(req,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    if not isinstance(data,list):print(f"❌ {data}");return
    print(f"📊 Binance Futures PnL ({symbol.upper()})\n"+"="*65)
    if not data:print("  (거래 없음)");return
    total_pnl=0;total_fee=0
    for t in data[-30:]:
        dt=datetime.fromtimestamp(t["time"]/1000).strftime("%m-%d %H:%M")
        side="🟢 BUY" if t["side"]=="BUY" else "🔴 SELL"
        pnl=float(t.get("realizedPnl",0));fee=float(t.get("commission",0))
        price=float(t["price"]);qty=float(t["qty"])
        total_pnl+=pnl;total_fee+=fee
        if pnl!=0:
            print(f"  {dt} {side} {qty:.4f} @ ${price:,.2f}  PnL: {'🟢' if pnl>=0 else '🔴'}${pnl:,.2f}  Fee: ${fee:.4f}")
    print(f"\n{'='*65}")
    print(f"  Total Realized PnL: {'🟢' if total_pnl>=0 else '🔴'} ${total_pnl:,.2f}")
    print(f"  Total Fees: ${total_fee:,.4f}")
    print(f"  Net PnL: {'🟢' if (total_pnl-total_fee)>=0 else '🔴'} ${total_pnl-total_fee:,.2f}")
