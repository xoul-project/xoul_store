def run(coins: str = "BTC,ETH,SOL,XRP,DOGE"):
    """
    coins: Coin symbols (comma separated) (default: BTC,ETH,SOL,XRP,DOGE)
    """
    import urllib.request,json
    coin_list=[c.strip().upper() for c in coins.split(",")]
    # 1) Upbit KRW prices
    upbit_mkts=",".join([f"KRW-{c}" for c in coin_list])
    try:
        req=urllib.request.Request(f"https://api.upbit.com/v1/ticker?markets={upbit_mkts}")
        req.add_header("Accept","application/json")
        with urllib.request.urlopen(req,timeout=10) as r:upbit_data=json.loads(r.read())
    except Exception as e:print(f"❌ Upbit: {e}");return
    upbit_prices={t["market"].replace("KRW-",""):t.get("trade_price",0) for t in upbit_data}
    # 2) Binance USDT prices
    try:
        with urllib.request.urlopen("https://api.binance.com/api/v3/ticker/price",timeout=10) as r:
            bn_data=json.loads(r.read())
    except Exception as e:print(f"❌ Binance: {e}");return
    bn_prices={}
    for t in bn_data:
        sym=t["symbol"]
        for c in coin_list:
            if sym==f"{c}USDT":bn_prices[c]=float(t["price"])
    # 3) USD/KRW exchange rate
    try:
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/USD",timeout=10) as r:
            fx=json.loads(r.read())
        usd_krw=fx.get("rates",{}).get("KRW",1350)
    except:usd_krw=1350
    print("🥟 Kimchi Premium (김치 프리미엄)\n"+"="*65)
    print(f"  USD/KRW: ₩{usd_krw:,.2f}\n")
    print(f"  {'Coin':<8}{'Upbit (₩)':>14}{'Binance ($)':>14}{'Binance (₩)':>14}{'Premium':>10}")
    print("  "+"-"*60)
    for c in coin_list:
        up=upbit_prices.get(c,0);bn=bn_prices.get(c,0)
        if up and bn:
            bn_krw=bn*usd_krw
            prem=(up-bn_krw)/bn_krw*100
            icon="🔴" if prem>3 else "🟢" if prem<-1 else "⚪"
            print(f"  {c:<8}₩{up:>12,.0f}${bn:>12,.2f}₩{bn_krw:>12,.0f}{icon}{prem:>+8.2f}%")
        else:
            print(f"  {c:<8}  (데이터 없음)")
    print(f"\n  ℹ️ Premium > 3% 🔴 고프리미엄 | < -1% 🟢 역프리미엄")
