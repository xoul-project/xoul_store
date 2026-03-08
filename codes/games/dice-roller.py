def run(dice: str = "2d6+3"):
    """
    dice: Dice notation (default: 2d6+3)
    """
    import random,re
    print(f"\U0001f3b2 Dice: {dice}\n"+"="*40)
    m=re.match(r'(\d+)d(\d+)([+-]\d+)?',dice)
    if not m:print('\u274c Format: NdS+M (e.g. 2d6+3)');exit()
    n,s,mod=int(m[1]),int(m[2]),int(m[3]or 0)
    rolls=[random.randint(1,s)for _ in range(n)]
    total=sum(rolls)+mod
    print(f"  Rolls: {rolls}\n  Sum: {sum(rolls)} + {mod} = {total}")
    if n>1:print(f"  Min possible: {n+mod}\n  Max possible: {n*s+mod}")