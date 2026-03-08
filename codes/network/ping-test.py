def run(hosts: str = "google.com,cloudflare.com,github.com"):
    """
    hosts: Hosts (comma separated) (default: google.com,cloudflare.com,github.com)
    """
    import subprocess
    print("\U0001f4e1 Ping Test\n"+"="*40)
    for h in hosts.split(','):
        h=h.strip()
        try:
            r=subprocess.run(['ping','-c','3',h],capture_output=True,text=True,timeout=10)
            for l in r.stdout.split('\n'):
                if 'avg' in l or 'rtt' in l:print(f"  {h}: {l.strip()}");break
            else:print(f"  {h}: {r.stdout.strip().split(chr(10))[-1]}")
        except Exception as e:print(f"  {h}: \u274c {e}")