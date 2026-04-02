def run(markets: str = "KRW-BTC,KRW-ETH,KRW-SOL,KRW-XRP,KRW-DOGE"):
    """
    markets: Market codes (comma separated) (default: KRW-BTC,KRW-ETH,KRW-SOL,KRW-XRP,KRW-DOGE)
    """
    import urllib.request,json
    mkt_list=[m.strip().upper() for m in markets.split(",")]
    mkt_param=",".join(mkt_list)
    try:
        req=urllib.request.Request(f"https://api.upbit.com/v1/ticker?markets={mkt_param}")
        req.add_header("Accept","application/json")
        with urllib.request.urlopen(req,timeout=10) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    print("🇰🇷 Upbit KRW Market Ticker\n"+"="*65)
    print(f"  {'Market':<12}{'Price (₩)':>14}{'24h %':>10}{'High':>14}{'Low':>14}")
    print("  "+"-"*62)
    for t in data:
        m=t["market"];p=t.get("trade_price",0)
        ch=t.get("signed_change_rate",0)*100
        hi=t.get("high_price",0);lo=t.get("low_price",0)
        vol=t.get("acc_trade_price_24h",0)
        icon='🟢' if ch>=0 else '🔴'
        coin=m.replace("KRW-","")
        print(f"  {icon}{coin:<11}₩{p:>12,.0f}{ch:>+9.2f}%₩{hi:>12,.0f}₩{lo:>12,.0f}")
    print()
    for t in data:
        vol=t.get("acc_trade_price_24h",0)
        coin=t["market"].replace("KRW-","")
        print(f"  {coin} 24h Vol: ₩{vol:>16,.0f}")
