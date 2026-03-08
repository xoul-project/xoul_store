def run(number: str = "97"):
    """
    number: Number (default: 97)
    """
    n=int(number)
    def is_prime(x):
        if x<2:return False
        for i in range(2,int(x**0.5)+1):
            if x%i==0:return False
        return True
    print(f"\U0001f522 Prime Check: {n}\n"+"="*40)
    print(f"  {n} is {'\u2705 PRIME' if is_prime(n) else '\u274c NOT prime'}")
    if not is_prime(n):
        factors=[]
        x=n
        for i in range(2,int(x**0.5)+1):
            while x%i==0:factors.append(i);x//=i
        if x>1:factors.append(x)
        print(f"  Factors: {' \u00d7 '.join(map(str,factors))}")
    print('\n  Nearby primes: ',end='')
    found=0;x=max(2,n-10)
    while found<5:
        if is_prime(x):print(x,end=' ');found+=1
        x+=1