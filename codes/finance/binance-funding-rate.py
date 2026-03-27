def run(symbols: str = "BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,BNBUSDT"):
    """
    symbols: Futures pairs (comma separated) (default: BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,DOGEUSDT,BNBUSDT)
    """
    import urllib.request,json
    from datetime import datetime
    BASE="https://fapi.binance.com"
    sym_list=[s.strip().upper() for s in symbols.split(",")]
    try:
        with urllib.request.urlopen(f"{BASE}/fapi/v1/premiumIndex",timeout=10) as r:
            data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    print("💸 Binance Funding Rates\n"+"="*65)
    print(f"  {'Symbol':<12}{'Mark Price':>14}{'Funding Rate':>14}{'Next Fund':>20}")
    print("  "+"-"*60)
    for d in data:
        if d["symbol"] in sym_list:
            mark=float(d.get("markPrice",0))
            rate=float(d.get("lastFundingRate",0))*100
            nxt=d.get("nextFundingTime",0)
            nxt_str=datetime.fromtimestamp(nxt/1000).strftime("%H:%M:%S") if nxt else "?"
            icon="🟢" if rate>=0 else "🔴"
            print(f"  {d['symbol']:<12}${mark:>12,.2f}{icon}{rate:>+12.4f}%  {nxt_str:>18}")
    print(f"\n  ℹ️ +rate = longs pay shorts | -rate = shorts pay longs")
