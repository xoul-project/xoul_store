def run(n: str = "20"):
    """
    n: Count (default: 20)
    """
    n=int(n)
    a,b=0,1;seq=[a]
    for _ in range(n-1):a,b=b,a+b;seq.append(a)
    print(f"\U0001f300 Fibonacci ({n})\n"+"="*40)
    for i,v in enumerate(seq):print(f"  F({i})={v:,}",end='  ')
        if(i+1)%5==0:print()
    if len(seq)>=2:print(f"\n\n  Golden ratio: {seq[-1]/seq[-2]:.10f}\n  Phi:          1.6180339887...")