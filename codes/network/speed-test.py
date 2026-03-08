def run():
    import urllib.request,time
    url='http://speedtest.tele2.net/1MB.zip'
    print("\u26a1 Speed Test\n"+"="*40+"\n  Downloading 1MB test file...")
    t0=time.time()
    try:
        with urllib.request.urlopen(url,timeout=30) as r:data=r.read()
        elapsed=time.time()-t0;size=len(data)
        mbps=(size*8)/(elapsed*1000000)
        print(f"  Size: {size:,} bytes\n  Time: {elapsed:.2f}s\n  Speed: {mbps:.2f} Mbps")
    except Exception as e:print(f"  \u274c {e}")