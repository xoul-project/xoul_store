def run():
    import urllib.request,json,os
    ARENA=os.environ.get('ARENA_URL','https://www.xoulai.net:8081')
    try:
        with urllib.request.urlopen(f'{ARENA}/arena/games?status=finished&limit=20',timeout=10) as r:data=json.loads(r.read())
    except Exception as e:print(f'\u274c {e}');exit()
    games=data.get('games',[])
    print(f"\U0001f4ca Arena Stats ({len(games)} recent games)\n"+"="*45)
    wins={}
    for g in games:
        w=g.get('winner','?')
        print(f"  {g['id'][:8]} | Winner: {w} | Players: {g.get('player_count','?')}")
        wins[w]=wins.get(w,0)+1
    if wins:
        print('\n  Win counts:')
        for w,c in sorted(wins.items(),key=lambda x:-x[1]):print(f"    {w}: {c}")