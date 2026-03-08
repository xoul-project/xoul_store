def run(url: str = "https://google.com"):
    """
    url: URL (default: https://google.com)
    """
    import urllib.request,time
    print(f"\U0001f3e5 HTTP Check: {url}\n"+"="*40)
    t0=time.time()
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=15) as r:
            ms=(time.time()-t0)*1000;sz=len(r.read())
            print(f"  Status: \u2705 {r.status}\n  Speed: {ms:.0f}ms\n  Size: {sz:,}B\n  Server: {r.headers.get('Server','?')}")
    except Exception as e:print(f"  \u274c {e}")