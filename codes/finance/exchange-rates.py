def run(base: str = "USD"):
    """
    base: Base currency (default: USD)
    """
    import urllib.request,json
    with urllib.request.urlopen(f"https://open.er-api.com/v6/latest/{base}",timeout=10) as r:data=json.loads(r.read())
    print(f"\U0001f4b1 Exchange Rates ({base})\n"+"="*45)
    for t in["KRW","JPY","EUR","GBP","CNY","CHF","CAD","AUD","SGD"]:
        if t in data.get("rates",{}):print(f"  {base}/{t}: {data['rates'][t]:>12,.4f}")
    print(f"\nUpdated: {data.get('time_last_update_utc','?')}")