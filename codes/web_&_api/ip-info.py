def run():
    import urllib.request,json
    with urllib.request.urlopen("https://ipinfo.io/json",timeout=10) as r:d=json.loads(r.read())
    print("\U0001f30d IP Info\n"+"="*40)
    for k in["ip","hostname","city","region","country","loc","org","timezone"]:
        if k in d:print(f"  {k:<12}: {d[k]}")