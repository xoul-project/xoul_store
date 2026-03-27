def run():
    """
    (no params)
    """
    import urllib.request,json
    try:
        req=urllib.request.Request("https://api.upbit.com/v1/market/all?isDetails=false")
        req.add_header("Accept","application/json")
        with urllib.request.urlopen(req,timeout=10) as r:markets=json.loads(r.read())
        krw_mkts=[m["market"] for m in markets if m["market"].startswith("KRW-")]
        mkt_param=",".join(krw_mkts)
        req2=urllib.request.Request(f"https://api.upbit.com/v1/ticker?markets={mkt_param}")
        req2.add_header("Accept","application/json")
        with urllib.request.urlopen(req2,timeout=15) as r:data=json.loads(r.read())
    except Exception as e:print(f"❌ {e}");return
    ranked=sorted(data,key=lambda x:x.get("signed_change_rate",0),reverse=True)
    print("🇰🇷 Upbit KRW Market Index\n"+"="*60)
    print(f"\n  🚀 TOP 10 상승")
    print(f"  {'Coin':<8}{'Price (₩)':>14}{'24h %':>10}{'Volume (₩)':>18}")
    print("  "+"-"*50)
    for t in ranked[:10]:
        coin=t["market"].replace("KRW-","")
        p=t.get("trade_price",0);ch=t.get("signed_change_rate",0)*100
        vol=t.get("acc_trade_price_24h",0)
        print(f"  🟢{coin:<7}₩{p:>12,.0f}{ch:>+9.2f}%₩{vol:>16,.0f}")
    print(f"\n  📉 TOP 10 하락")
    print(f"  {'Coin':<8}{'Price (₩)':>14}{'24h %':>10}{'Volume (₩)':>18}")
    print("  "+"-"*50)
    for t in ranked[-10:]:
        coin=t["market"].replace("KRW-","")
        p=t.get("trade_price",0);ch=t.get("signed_change_rate",0)*100
        vol=t.get("acc_trade_price_24h",0)
        print(f"  🔴{coin:<7}₩{p:>12,.0f}{ch:>+9.2f}%₩{vol:>16,.0f}")
    up=sum(1 for t in data if t.get("signed_change_rate",0)>0)
    dn=sum(1 for t in data if t.get("signed_change_rate",0)<0)
    flat=len(data)-up-dn
    print(f"\n  📊 Market: 🟢 {up} up / 🔴 {dn} down / ⚪ {flat} flat (total {len(data)})")
