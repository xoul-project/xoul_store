def run():
    import urllib.request,json
    try:
        with urllib.request.urlopen("https://api.etherscan.io/api?module=gastracker&action=gasoracle",timeout=10) as r:g=json.loads(r.read()).get("result",{})
        print(f"\u26fd ETH Gas\n"+"="*40)
        print(f"  \U0001f422 Low:  {g.get('SafeGasPrice','?')} Gwei\n  \U0001f6b6 Avg:  {g.get('ProposeGasPrice','?')} Gwei\n  \U0001f680 Fast: {g.get('FastGasPrice','?')} Gwei")
    except Exception as e:print(f"\u274c {e}")