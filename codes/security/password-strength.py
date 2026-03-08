def run(password: str):
    """
    password: Password to check
    """
    import math,re,string
    print(f"\U0001f4aa Password Strength\n"+"="*40)
    pool=0
    if re.search(r'[a-z]',password):pool+=26;print('  \u2705 Lowercase')
    else:print('  \u274c No lowercase')
    if re.search(r'[A-Z]',password):pool+=26;print('  \u2705 Uppercase')
    else:print('  \u274c No uppercase')
    if re.search(r'\d',password):pool+=10;print('  \u2705 Digits')
    else:print('  \u274c No digits')
    if re.search(r'[^a-zA-Z0-9]',password):pool+=32;print('  \u2705 Symbols')
    else:print('  \u274c No symbols')
    entropy=len(password)*math.log2(max(pool,1))
    level='Weak' if entropy<40 else 'Fair' if entropy<60 else 'Strong' if entropy<80 else 'Very Strong'
    print(f"\n  Length: {len(password)}\n  Entropy: {entropy:.1f} bits\n  Rating: {level}")