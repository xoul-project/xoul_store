def run(target_date: str = "2025-12-31"):
    """
    target_date: Target date (YYYY-MM-DD) (default: 2025-12-31)
    """
    from datetime import datetime
    target=datetime.strptime(target_date,'%Y-%m-%d')
    now=datetime.now();diff=target-now
    print(f"\u23f3 D-Day: {target_date}\n"+"="*40)
    if diff.total_seconds()>0:
        d=diff.days;h=diff.seconds//3600;m=(diff.seconds%3600)//60
        print(f"  D-{d} ({d}d {h}h {m}m left)")
    else:
        print(f"  D+{abs(diff.days)} (passed {abs(diff.days)} days ago)")