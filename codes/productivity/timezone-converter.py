def run():
    from datetime import datetime,timezone,timedelta
    zones={'UTC':0,'KST(Seoul)':9,'JST(Tokyo)':9,'CST(Beijing)':8,'SGT':8,'IST(India)':5.5,'CET(Europe)':1,'GMT(London)':0,'EST(NewYork)':-5,'PST(LA)':-8}
    print("\U0001f550 World Clocks\n"+"="*45)
    now=datetime.now(timezone.utc)
    for name,off in zones.items():
        t=now+timedelta(hours=off)
        print(f"  {name:<16} {t.strftime('%Y-%m-%d %H:%M:%S')} (UTC{off:+.1f})")