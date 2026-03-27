def run(coins: str = "bitcoin,ethereum,solana,ripple,dogecoin"):
    """
    coins: Coin IDs (comma separated) (default: bitcoin,ethereum,solana,ripple,dogecoin)
    """
    import urllib.request,json
    url=f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd,krw&include_24hr_change=true"
    with urllib.request.urlopen(url,timeout=10) as r:data=json.loads(r.read())
    print("\U0001f4ca Crypto Prices\n"+"="*50)
    for c,v in data.items():
        usd=v.get("usd",0);krw=v.get("krw",0);ch=v.get("usd_24h_change",0)
        icon='\U0001f7e2' if ch>=0 else '\U0001f534'
        print(f"  {icon} {c.upper():<12}${usd:>10,.2f} \u20a9{krw:>14,.0f} ({ch:+.1f}%)")