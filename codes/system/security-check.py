def run():
    """
    SSH 로그인 기록, 실패 시도, 열린 포트를 점검합니다.
    Check SSH login history, failed attempts, and open ports.
    """
    import subprocess
    print("\U0001f6e1 Security Check\n" + "=" * 45)
    
    print("\n\U0001f511 Recent SSH Logins:")
    try:
        out = subprocess.run(["last", "-n", "5", "-w"], capture_output=True, text=True, timeout=5)
        for line in out.stdout.strip().split("\n")[:5]:
            if line.strip():
                print(f"  {line}")
    except:
        print("  (unavailable)")
    
    print("\n\u26a0 Failed Login Attempts (last 24h):")
    try:
        out = subprocess.run(
            ["journalctl", "-u", "ssh", "--since", "24h ago", "--no-pager", "-q"],
            capture_output=True, text=True, timeout=5
        )
        fails = [l for l in out.stdout.split("\n") if "Failed" in l or "Invalid" in l]
        if fails:
            print(f"  {len(fails)} failed attempts")
            for f in fails[-3:]:
                print(f"  \U0001f534 {f.strip()[-80:]}")
        else:
            print("  \u2705 No failed attempts")
    except:
        print("  (unavailable)")
    
    print("\n\U0001f310 Listening Ports:")
    try:
        out = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
        for line in out.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 4:
                print(f"  {parts[3]:<25} {parts[-1] if len(parts) > 5 else ''}")
    except:
        print("  (unavailable)")
