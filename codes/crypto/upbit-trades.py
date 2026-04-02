def run(market: str = "KRW-BTC", count: str = "20"):
    """
    market: Market code (default: KRW-BTC)
    count: Number of trades (default: 20)
    """
    import urllib.request,json
    mkt=market.strip().upper();cnt=min(int(count),50)
    try:
        req=urllib.request.Request(f"https://api.upbit.com/v1/trades/ticks?market={mkt}&count={cnt}")
        req.add_header("Accept","application/json")
        with urllib.request.urlopen(req,timeout=10) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    print(f"🔄 Upbit Recent Trades ({mkt})\n"+"="*60)
    print(f"  {'Time':>10}{'Side':>8}{'Price':>14}{'Volume':>14}{'Total':>16}")
    print("  "+"-"*58)
    for t in data:
        tm=t.get("trade_time_utc","?")[:8]
        side="🟢 BUY" if t.get("ask_bid")=="BID" else "🔴 SELL"
        price=t.get("trade_price",0);vol=t.get("trade_volume",0)
        total=price*vol
        print(f"  {tm:>10}{side:>8}₩{price:>12,.0f}{vol:>13.4f}₩{total:>14,.0f}")
    if data:
        hi=max(t["trade_price"] for t in data);lo=min(t["trade_price"] for t in data)
        tot_vol=sum(t["trade_volume"] for t in data)
        print(f"\n  Range: ₩{lo:,.0f} ~ ₩{hi:,.0f}  Total Vol: {tot_vol:.4f}")
