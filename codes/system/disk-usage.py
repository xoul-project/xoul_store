def run():
    import subprocess,os
    print("\U0001f4be System Status\n"+"="*40)
    for label,cmd in{"Disk":"df -h /","Memory":"free -h","Uptime":"uptime -p","Load":"cat /proc/loadavg","Kernel":"uname -r"}.items():
        try:
            r=subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=5)
            if r.stdout.strip():print(f"\n  [{label}]\n  {r.stdout.strip()}")
        except:pass