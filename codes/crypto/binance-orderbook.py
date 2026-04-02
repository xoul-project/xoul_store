def run(symbol: str = "BTCUSDT", limit: str = "10"):
    """
    symbol: Trading pair (default: BTCUSDT)
    limit: Number of levels (default: 10)
    """
    import urllib.request,json
    sym=symbol.upper();lim=int(limit)
    try:
        with urllib.request.urlopen(f"https://api.binance.com/api/v3/depth?symbol={sym}&limit={lim}",timeout=10) as r:
            data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    bids=data.get("bids",[]);asks=data.get("asks",[])
    print(f"📖 Binance Order Book ({sym})\n"+"="*55)
    print(f"  {'ASK (매도)':^55}")
    for p,q in reversed(asks[:lim]):
        bar="█"*min(int(float(q)*2),20)
        print(f"  🔴 ${float(p):>10,.2f}  {float(q):>12.4f}  {bar}")
    print(f"  {'─'*50}")
    for p,q in bids[:lim]:
        bar="█"*min(int(float(q)*2),20)
        print(f"  🟢 ${float(p):>10,.2f}  {float(q):>12.4f}  {bar}")
    print(f"  {'BID (매수)':^55}")
    if bids and asks:
        spread=float(asks[0][0])-float(bids[0][0])
        pct=spread/float(asks[0][0])*100
        print(f"\n  Spread: ${spread:,.2f} ({pct:.4f}%)")
