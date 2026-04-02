def run(symbols: str = "BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,BNBUSDT"):
    """
    symbols: Trading pairs (comma separated) (default: BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,BNBUSDT)
    """
    import urllib.request,json
    BASE="https://api.binance.com"
    sym_list=[s.strip().upper() for s in symbols.split(",")]
    try:
        with urllib.request.urlopen(f"{BASE}/api/v3/ticker/24hr",timeout=10) as r:
            data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    print("📊 Binance 24h Ticker\n"+"="*65)
    print(f"  {'Symbol':<12}{'Price':>12}{'24h %':>10}{'High':>12}{'Low':>12}{'Vol':>14}")
    print("  "+"-"*60)
    for t in data:
        if t["symbol"] in sym_list:
            p=float(t["lastPrice"]);ch=float(t["priceChangePercent"])
            hi=float(t["highPrice"]);lo=float(t["lowPrice"])
            vol=float(t["quoteVolume"])
            icon='🟢' if ch>=0 else '🔴'
            print(f"  {icon}{t['symbol']:<11}${p:>10,.2f}{ch:>+9.2f}%${hi:>10,.2f}${lo:>10,.2f}${vol:>12,.0f}")
