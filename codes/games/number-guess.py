def run(max_num: str = "100"):
    """
    max_num: Max number (default: 100)
    """
    import random
    mx=int(max_num);target=random.randint(1,mx)
    print(f"\U0001f522 Guess the Number (1-{mx})\n"+"="*40)
    lo,hi,tries=1,mx,0
    while lo<=hi:
        guess=(lo+hi)//2;tries+=1
        if guess==target:print(f"  #{tries}: {guess} \U0001f389 CORRECT!");break
        elif guess<target:print(f"  #{tries}: {guess} \u2b06 Too low");lo=guess+1
        else:print(f"  #{tries}: {guess} \u2b07 Too high");hi=guess-1
    print(f"\n  Answer: {target} (found in {tries} tries)")