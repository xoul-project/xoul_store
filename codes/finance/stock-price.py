def run(symbol: str = "AAPL"):
    """
    symbol: Ticker symbol (default: AAPL)
    """
    import urllib.request,json
    req=urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d",headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req,timeout=10) as r:data=json.loads(r.read())
        m=data["chart"]["result"][0]["meta"];p=m["regularMarketPrice"];pv=m.get("chartPreviousClose",p);ch=((p-pv)/pv)*100
        print(f"\U0001f4ca {symbol.upper()}\n"+"="*40)
        print(f"  Price: ${p:,.2f}\n  Change: {'\U0001f7e2'if ch>=0 else'\U0001f534'} {ch:+.2f}%\n  Exchange: {m.get('exchangeName','?')}")
    except Exception as e:print(f"\u274c {e}")