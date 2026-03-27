def run(api_key: str = "", api_secret: str = ""):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    if not api_key or not api_secret:
        print("❌ api_key, api_secret 필요. recall('binance api')로 조회하세요.");return
    BASE="https://api.binance.com"
    ts=int(time.time()*1000);qs=f"timestamp={ts}"
    sig=hmac.new(api_secret.encode(),qs.encode(),hashlib.sha256).hexdigest()
    req=urllib.request.Request(f"{BASE}/api/v3/account?{qs}&signature={sig}")
    req.add_header("X-MBX-APIKEY",api_key)
    try:
        with urllib.request.urlopen(req,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    print("💰 Binance Spot Balance\n"+"="*55)
    total_btc=0
    for b in data.get("balances",[]):
        free=float(b["free"]);locked=float(b["locked"]);total=free+locked
        if total>0.00001:
            print(f"  {b['asset']:<8} Free: {free:>14.6f}  Locked: {locked:>14.6f}")
    print(f"\n📊 Account Type: {data.get('accountType','?')}")
    print(f"🔄 Can Trade: {data.get('canTrade',False)}")
