def run(market: str = "KRW-BTC"):
    """
    market: Market code (default: KRW-BTC)
    """
    import urllib.request,json
    mkt=market.strip().upper()
    try:
        req=urllib.request.Request(f"https://api.upbit.com/v1/orderbook?markets={mkt}")
        req.add_header("Accept","application/json")
        with urllib.request.urlopen(req,timeout=10) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    if not data:print("❌ 데이터 없음");return
    ob=data[0];units=ob.get("orderbook_units",[])
    print(f"📖 Upbit Order Book ({mkt})\n"+"="*55)
    print(f"  {'ASK (매도)':^55}")
    asks=[(u["ask_price"],u["ask_size"]) for u in units]
    for p,q in reversed(asks):
        bar="█"*min(int(q*5),20)
        print(f"  🔴 ₩{p:>12,.0f}  {q:>12.4f}  {bar}")
    print(f"  {'─'*50}")
    for u in units:
        p=u["bid_price"];q=u["bid_size"]
        bar="█"*min(int(q*5),20)
        print(f"  🟢 ₩{p:>12,.0f}  {q:>12.4f}  {bar}")
    print(f"  {'BID (매수)':^55}")
    total_ask=sum(u["ask_size"] for u in units)
    total_bid=sum(u["bid_size"] for u in units)
    ratio=total_bid/(total_ask+0.0001)*100
    print(f"\n  매수/매도 비율: {ratio:.1f}% ({'매수 우세 🟢' if ratio>100 else '매도 우세 🔴'})")
