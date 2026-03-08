def run(game_id: str):
    """
    game_id: Game ID to watch
    """
    import urllib.request,json,time,os
    ARENA=os.environ.get('ARENA_URL','http://15.165.31.212:8081')
    def get(p):
        try:
            with urllib.request.urlopen(f'{ARENA}{p}',timeout=10) as r:return json.loads(r.read())
        except:return{}
    print(f"\U0001f441 Spectating: {game_id}\n"+"="*45)
    seen=0
    for _ in range(300):
        state=get(f'/arena/games/{game_id}/state')
        if state.get('status')=='finished':print(f"\n\U0001f3c1 Game over! Winner: {state.get('winner','?')}");break
        log=state.get('chat_log',[])
        for msg in log[seen:]:
            t=msg.get('type','');p=msg.get('player','?');d=msg.get('data',{})
            if t=='speak':print(f"  \U0001f4ac {p}: {d.get('message','')[:80]}")
            elif t=='vote':print(f"  \U0001f5f3 {p} \u2192 {d.get('target','?')}")
            elif t=='eliminated':print(f"  \u274c {p} eliminated")
            elif t=='system':print(f"  \u2139 {d.get('message','')}")
        seen=len(log)
        time.sleep(3)