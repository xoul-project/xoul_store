def run(items: str = "A,B,C,D,E", count: str = "1"):
    """
    items: Items (comma separated) (default: A,B,C,D,E)
    count: Pick count (default: 1)
    """
    import random
    lst=[x.strip()for x in items.split(',')if x.strip()]
    n=min(int(count),len(lst))
    picks=random.sample(lst,n)
    print(f"\U0001f3b2 Random Pick ({n}/{len(lst)})\n"+"="*40)
    for i,p in enumerate(picks):print(f"  {i+1}. \U0001f3af {p}")