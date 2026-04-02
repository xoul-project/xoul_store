def run(api_key: str = "", api_secret: str = "", symbol: str = "BTCUSDT"):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    symbol: Trading pair (default: BTCUSDT)
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    if not api_key or not api_secret:
        print("❌ api_key, api_secret 필요. recall('binance api')로 조회하세요.");return
    BASE="https://api.binance.com"
    params={"symbol":symbol.upper(),"limit":"20","timestamp":str(int(time.time()*1000))}
    qs=urllib.parse.urlencode(params)
    sig=hmac.new(api_secret.encode(),qs.encode(),hashlib.sha256).hexdigest()
    req=urllib.request.Request(f"{BASE}/api/v3/myTrades?{qs}&signature={sig}")
    req.add_header("X-MBX-APIKEY",api_key)
    try:
        with urllib.request.urlopen(req,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    if not isinstance(data,list):print(f"❌ {data}");return
    print(f"📜 Binance Trade History ({symbol.upper()})\n"+"="*65)
    if not data:print("  (거래 내역 없음)");return
    for t in reversed(data[-20:]):
        from datetime import datetime
        dt=datetime.fromtimestamp(t["time"]/1000).strftime("%m-%d %H:%M")
        side="🟢 BUY" if t.get("isBuyer") else "🔴 SELL"
        price=float(t["price"]);qty=float(t["qty"]);total=price*qty
        fee=float(t.get("commission",0));fee_asset=t.get("commissionAsset","")
        print(f"  {dt} {side} {qty:.6f} @ ${price:,.2f} = ${total:,.2f} (fee: {fee:.6f} {fee_asset})")
