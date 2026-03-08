def run(filter: str = ""):
    """
    filter: Filter keyword (empty=all) (default: )
    """
    import os
    print(f"\U0001f527 Environment Variables\n"+"="*40)
    vars=sorted(os.environ.items())
    if filter:
        vars=[(k,v)for k,v in vars if filter.lower()in k.lower()or filter.lower()in v.lower()]
        print(f"  Filter: '{filter}' ({len(vars)} matches)")
    for k,v in vars:print(f"  {k}={v[:80]}")