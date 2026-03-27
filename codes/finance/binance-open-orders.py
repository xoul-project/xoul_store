def run(api_key: str = "", api_secret: str = "", symbol: str = ""):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    symbol: Trading pair (empty=all) (default: )
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    if not api_key or not api_secret:
        print("❌ api_key, api_secret 필요. recall('binance api')로 조회하세요.");return
    BASE="https://api.binance.com"
    params={"timestamp":str(int(time.time()*1000))}
    if symbol:params["symbol"]=symbol.upper()
    qs=urllib.parse.urlencode(params)
    sig=hmac.new(api_secret.encode(),qs.encode(),hashlib.sha256).hexdigest()
    req=urllib.request.Request(f"{BASE}/api/v3/openOrders?{qs}&signature={sig}")
    req.add_header("X-MBX-APIKEY",api_key)
    try:
        with urllib.request.urlopen(req,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    if not isinstance(data,list):print(f"❌ {data}");return
    title=f"📋 Open Orders" + (f" ({symbol.upper()})" if symbol else " (All)")
    print(f"{title}\n"+"="*60)
    if not data:print("  (미체결 주문 없음)");return
    for o in data:
        from datetime import datetime
        dt=datetime.fromtimestamp(o["time"]/1000).strftime("%m-%d %H:%M")
        side="🟢 BUY" if o["side"]=="BUY" else "🔴 SELL"
        price=float(o["price"]);qty=float(o["origQty"]);filled=float(o.get("executedQty",0))
        print(f"  {o['symbol']} {side} {o['type']}")
        print(f"    Price: ${price:,.2f}  Qty: {qty:.6f}  Filled: {filled:.6f}  [{dt}]")
