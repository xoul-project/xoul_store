def run(domain: str = "google.com"):
    """
    domain: Domain (default: google.com)
    """
    import urllib.request,json
    with urllib.request.urlopen(f"https://dns.google/resolve?name={domain}&type=A",timeout=10) as r:d=json.loads(r.read())
    print(f"\U0001f50d DNS: {domain}\n"+"="*40)
    for a in d.get("Answer",[]):print(f"  {a.get('name','')} \u2192 {a.get('data','')} (TTL:{a.get('TTL','')}s)")
    if not d.get("Answer"):print("  (no records)")