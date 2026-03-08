def run(work_min: str = "25"):
    """
    work_min: Work minutes (default: 25)
    """
    import time
    w=int(work_min);b=5
    print(f"\U0001f345 Pomodoro: {w}min work + {b}min break\n"+"="*40)
    print(f"  \U0001f4aa WORK START")
    for s in range(w*60,0,-1):
        if s%(60)==0:print(f"  {s//60}:{s%60:02d} remaining...")
        time.sleep(1)
    print(f"  \u2705 Work done!\n\n  \u2615 BREAK ({b}min)")
    for s in range(b*60,0,-1):
        if s%(60)==0:print(f"  {s//60}:{s%60:02d} remaining...")
        time.sleep(1)
    print(f"  \u2705 Break done! Great job!")