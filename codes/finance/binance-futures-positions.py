def run(api_key: str = "", api_secret: str = ""):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    if not api_key or not api_secret:
        print("❌ api_key, api_secret 필요. recall('binance api')로 조회하세요.");return
    BASE="https://fapi.binance.com"
    ts=int(time.time()*1000);qs=f"timestamp={ts}"
    sig=hmac.new(api_secret.encode(),qs.encode(),hashlib.sha256).hexdigest()
    req=urllib.request.Request(f"{BASE}/fapi/v2/positionRisk?{qs}&signature={sig}")
    req.add_header("X-MBX-APIKEY",api_key)
    try:
        with urllib.request.urlopen(req,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    if not isinstance(data,list):print(f"❌ {data}");return
    open_pos=[p for p in data if float(p.get("positionAmt",0))!=0]
    print("📈 Binance Futures Positions\n"+"="*60)
    if not open_pos:
        print("  (오픈 포지션 없음)");return
    total_pnl=0
    for p in open_pos:
        amt=float(p["positionAmt"]);side="🟢 LONG" if amt>0 else "🔴 SHORT"
        entry=float(p.get("entryPrice",0));mark=float(p.get("markPrice",0))
        pnl=float(p.get("unRealizedProfit",0));lev=p.get("leverage","?")
        liq=p.get("liquidationPrice","N/A");total_pnl+=pnl
        print(f"  {p['symbol']}")
        print(f"    {side} x{lev}  Size: {abs(amt):.4f}")
        print(f"    Entry: ${entry:,.2f}  Mark: ${mark:,.2f}")
        print(f"    PnL: {'🟢' if pnl>=0 else '🔴'} ${pnl:,.2f}  Liq: ${liq}")
    print(f"\n{'='*60}")
    print(f"  Total Unrealized PnL: {'🟢' if total_pnl>=0 else '🔴'} ${total_pnl:,.2f}")
