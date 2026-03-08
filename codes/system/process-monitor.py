def run(count: str = "10"):
    """
    count: Number of processes (default: 10)
    """
    import subprocess
    n=int(count)
    print(f"\U0001f4cb Top {n} Processes\n"+"="*50)
    for title,cmd in[("By CPU",f"ps aux --sort=-%cpu | head -{n+1}"),("By Memory",f"ps aux --sort=-%mem | head -{n+1}")]:
        print(f"\n  [{title}]")
        r=subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=5)
        for line in r.stdout.strip().split('\n'):print(f"  {line}")