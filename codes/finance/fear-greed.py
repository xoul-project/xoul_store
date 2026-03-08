def run():
    import urllib.request,json
    with urllib.request.urlopen("https://api.alternative.me/fng/?limit=7",timeout=10) as r:data=json.loads(r.read())
    print("\U0001f631 Fear & Greed Index\n"+"="*45)
    for d in data.get("data",[]):
        v=int(d["value"]);bar="\u2588"*int(v/5)+"\u2591"*(20-int(v/5))
        from datetime import datetime
        dt=datetime.fromtimestamp(int(d["timestamp"])).strftime("%Y-%m-%d")
        print(f"  {dt} [{bar}] {v}/100 ({d['value_classification']})")