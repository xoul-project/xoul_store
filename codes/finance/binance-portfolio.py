def run(api_key: str, api_secret: str):
    """
    api_key: Binance API Key
    api_secret: Binance API Secret
    """
    import hashlib,hmac,time,urllib.parse,urllib.request,json
    BASE_S="https://api.binance.com";BASE_F="https://fapi.binance.com"
    def _sign(qs,s):return hmac.new(s.encode(),qs.encode(),hashlib.sha256).hexdigest()
    def _req(base,ep,params=None,secret=None,key=None):
        params=params or {};params["timestamp"]=int(time.time()*1000);qs=urllib.parse.urlencode(params)
        if secret:qs+=f"&signature={_sign(qs,secret)}"
        req=urllib.request.Request(f"{base}{ep}?{qs}")
        if key:req.add_header("X-MBX-APIKEY",key)
        try:
            with urllib.request.urlopen(req,timeout=10) as r:return json.loads(r.read())
        except Exception as e:return{"error":str(e)}
    print("="*55+"\n\U0001f4b9 Binance Portfolio\n"+"="*55)
    print("\n\U0001f4b0 Prices:")
    t=_req(BASE_S,"/api/v3/ticker/24hr")
    if isinstance(t,list):
        for x in t:
            if x["symbol"]in["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","DOGEUSDT"]:
                p,c=float(x["lastPrice"]),float(x["priceChangePercent"]);print(f"  {'\U0001f7e2'if c>=0 else'\U0001f534'} {x['symbol']}: ${p:,.2f} ({c:+.2f}%)")
    print("\n\U0001f4bc Spot:")
    a=_req(BASE_S,"/api/v3/account",secret=api_secret,key=api_key)
    if"balances"in a:
        for b in a["balances"]:
            t=float(b["free"])+float(b["locked"])
            if t>0.0001:print(f"  {b['asset']:<8}{t:>14.6f}")
    elif"error"in a:print(f"  {a['error']}")
    print("\n\U0001f4c8 Futures:")
    pos=_req(BASE_F,"/fapi/v2/positionRisk",secret=api_secret,key=api_key)
    if isinstance(pos,list):
        op=[p for p in pos if float(p.get("positionAmt",0))!=0]
        for p in op:
            sd="LONG"if float(p["positionAmt"])>0 else"SHORT";pnl=float(p.get("unRealizedProfit",0))
            print(f"  {p['symbol']} {sd} x{p.get('leverage','?')} PnL:${pnl:,.2f}")
        if not op:print("  (no open positions)")
    print("\n\u2705 Done!")