def run(expression: str = "*/5 * * * *"):
    """
    expression: Cron expression (default: */5 * * * *)
    """
    parts=expression.split()
    if len(parts)!=5:print(f'\u274c Invalid: need 5 fields');exit()
    names=['Minute','Hour','Day','Month','Weekday']
    ranges=['0-59','0-23','1-31','1-12','0-7']
    print(f"\u23f0 Cron: {expression}\n"+"="*40)
    for n,v,r in zip(names,parts,ranges):
        if v=='*':desc='every'
        elif v.startswith('*/'):desc=f'every {v[2:]}'
        else:desc=v
        print(f"  {n:<10}: {v:<8} ({desc}, range: {r})")
    m,h,d,mo,w=parts
    print(f"\n  Summary: ",end='')
    if m.startswith('*/'):print(f"Every {m[2:]} minutes",end=' ')
    elif m=='0':print(f"At minute 0",end=' ')
    if h!='*':print(f"at hour {h}",end=' ')
    if d!='*':print(f"on day {d}",end=' ')
    print()